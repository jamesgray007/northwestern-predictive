# analyzing the Wisconsin Dells data using the 
# apriori program from Peter Harrington (2012)

# Harrington, P. (2012). Machine learning in action. Shelter Island, N.Y.: Manning. 
# open-source code from:  www.manning.com/MachineLearninginAction  (see Chapter 11)

# let's make our programs compatible with Python 3.0/1/2/3
from __future__ import division, print_function
from future_builtins import ascii, filter, hex, map, oct, zip

import numpy as np  # array operations
import pandas as pd  # pandas for data frame operations

# set maximum number of rows to twenty  
pd.options.display.max_rows = 20

# set paramteters for apriori algorithm
alpha = 0.10  # required level of support for apriori item sets
beta = 0.25  # required level of confidence for apriori rules
max_other_items =  2  # maximum other items in reported rule set
# frozen set is an immutable set
item_of_interest = frozenset(['shopping'])  # character string of item of interest

from mlia import apriori  # this brings in a subset of methods from apriori

# -------------------------------------------------
# Generate list of lists from Wisconsin Dells data
# -------------------------------------------------
# read in the Wisconsin Dells data
wi_dells = pd.read_csv('wisconsin_dells.csv')
print(wi_dells.shape)  # check the structure of the data frame

# list of activities for study
activity = ['shopping',	'antiquing', 'scenery',	'eatfine',
    'eatcasual', 'eatfamstyle',	'eatfastfood',	'museums',
    'indoorpool', 'outdoorpool', 'hiking', 'gambling',
    'boatswim',	'fishing', 'golfing', 'boattours', 'rideducks',
    'amusepark', 'minigolf', 'gocarting', 'waterpark', 
    'circusworld', 'tbskishow', 'helicopter', 'horseride',
    'standrock', 'outattract', 'nearbyattract', 'movietheater',	
    'concerttheater', 'barpubdance', 'shopbroadway', 'bungeejumping']
    
# work with a subset of the data columns corresponding to the activities
df = pd.DataFrame(wi_dells, columns = activity)
print(df.shape)  # check the structure of the data frame
print(df.head)  # examine the first few lines of the data frame

# YES activity cells of the data frame replaced by name of activity
# NO coded as missing data using numpy nan method
for index in range(len(activity)):
    activity_to_name = {'NO' : np.nan, 'YES' : activity[index]}
    df[activity[index]] = df[activity[index]].map(activity_to_name)

print(df.head)  # examine the first few lines of the recoded data frame 

# my_data is the list of lists structure that is needed 
# for input to the apriori algorithm
my_data = list()  # initialize list structure for list of lists

# loop through the rows of the data frame by index ix 
# creating the list of lists structure one activity basket at a time
# we use dropna() to omit missing data as coded nan from numpy

# generate the activity basket for this visitor
# and convert it to a list for each of the df.shape[0] visitors
for index in range(df.shape[0]):
    basket = list(df.ix[index].dropna())  # this list for one visitor
    my_data.append(basket)  # add this list to list of lists

# -------------------------------------------------
# Apply the apriori algorithm to the list of lists
# -------------------------------------------------
L, suppData = apriori.apriori(my_data)

print('Identified rules with support = ', alpha, 'and confidence = ', beta)
rules = apriori.generateRules(L, suppData, minConf = beta)

# search across the rule set starting with smaller sets
# and moving to larger and larger sets until no rules
# exist that satisfy the requirement of including item_of_interest

n_other_items = 1  # initialize reporting at one other item
while n_other_items <= max_other_items:
    print('\nRules with ', n_other_items, ' other item(s)')
    for item in L[n_other_items]:        
        if item.intersection(item_of_interest): print(item)
    n_other_items = n_other_items + 1    
    
    
