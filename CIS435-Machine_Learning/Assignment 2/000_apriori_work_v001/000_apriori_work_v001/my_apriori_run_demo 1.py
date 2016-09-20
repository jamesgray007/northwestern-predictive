# apriori demonstration using apriori program from Peter Harrington (2012)

# Harrington, P. (2012). Machine learning in action. Shelter Island, N.Y.: Manning. 
# open-source code from:  www.manning.com/MachineLearninginAction  (see Chapter 11)

# let's make our programs compatible with Python 3.0/1/2/3
from __future__ import division, print_function
from future_builtins import ascii, filter, hex, map, oct, zip

# set paramteters for apriori algorithm
alpha = 0.5  # required level of support for apriori item sets
beta = 0.75  # required level of confidence for apriori rules
max_other_items =  2  # maximum other items in reported rule set
# frozen set is an immutable set
item_of_interest = frozenset(['apples'])  # character string of item of interest

from mlia import apriori  # this brings in a subset of methods from apriori

my_data = [
['apples', 'carrots', 'diapers'], 
['beer', 'carrots', 'eggplant'], 
['apples', 'beer', 'carrots', 'eggplant'], 
['beer', 'eggplant']
]

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
    
n_other_items = 2  # initialize reporting at one other item
while n_other_items <= max_other_items:
    print('\nRules with ', n_other_items, ' other item(s)')
    for item in L[n_other_items]:        
        if item.intersection(item_of_interest): print(item)
    n_other_items = n_other_items + 1     
