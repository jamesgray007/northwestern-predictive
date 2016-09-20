# Assignment 1: James Gray - graymatter@u.northwestern.edu - July 2014
# 
# This Python program will use the Wisconsin Dells case study data to target
# potential Wisconsin Dells visitors to "The Ducks" tour. 

# here are a few of the packages we rely upon for work in predictive analytics
# import os  # operating system module
# import pandas as pd  # pandas for data frame operations
# import numpy as np  # arrays an math functions
# import scipy as sp  # statistics and more for science 
# import sklearn as sk  # machine learning tools
# import statsmodels.formula.api as smf  # for working with R-style formulas
# import statsmodels.api as sm  # for working with numpy arrays
# import matplotlib.pyplot as plt  # 2D plotting
# import networkx as nx # software for network analysis

# these modules should prove especially useful in this first assignment
import pandas as pd  # pandas for data frame operations
import numpy as np  # arrays an math functions
import sklearn as sk  # machine learning tools
import matplotlib.pyplot as plt  # 2D plotting

# use scikit-learn as our toolset for machine learning
import sklearn as sk  

# ----------------------------------
# DATA PREPARATION NOTES
# ----------------------------------
# 
# Data from the Wisconsin Dells case study were collected as part of a
# survey study in the summer of 1995. The study and survey data are described in

# Harrington, J. C. (2007). Wisconsin Dells. Madison, Wisconsin: 
#     Research Publishers.
# 
# the work below uses pandas... which provides the DataFrame data structure,
# a DataFrame is a 2-dimensional labeled data structure with 
# columns of potentially different types... like an R data frame or SQL table

# ----------------------------------------------------------
# READ IN DATA... Wisconsin Dells survey data
# ----------------------------------------------------------
# read in Wisconsin Dells survey data after we ensure that
# the comma-delimited text file is in our working directory
# this creates a pandas DataFrame object 
wi_dells_data = pd.read_csv("wisconsin_dells.csv")

print("\nContents of wi_dells_data object ---------------")
# examine the structure of this DataFrame object
print(wi_dells_data)

# ----------------------------------------------------------
# Focus on the Wisconsin Dells visitors who "rideducks"
# ----------------------------------------------------------

# to see the data we need to do a little work due to the large number of columns
# documentation for what we are doing here is available at
# http://pandas.pydata.org/pandas-docs/stable/basics.html?highlight=set_option
pd.set_option('display.max_columns', 11)  # to allow at most 11 columns of data output

# the Wisconsin Dells demographic data are provided in the first ten columns
# let's select those columns along with the column for rideducks, 
# this will give us 11 columns of data for our analysis
# let's use df as a shorthand for our working data frame
# a Python list is used to specify the columns of interest

df = pd.DataFrame(wi_dells_data, 
    columns = ["id", "nnights", "nadults", "nchildren", "planning", 
    "sex", "age", "education", "income", "region", "rideducks"])
    
print("\nContents of the working data frame df---------------")
# examine the structure of this DataFrame object
print(df)    
    
# print the first five rows of the DataFrame
print(pd.DataFrame.head(df))  # note NaN values for missing data

# cross-tabulation for sex of respondent and engaging in bungeejumping
print(pd.crosstab(df.sex, df.rideducks))

# -----------------------------------------------------------------------
# Data Cleansing and Transformation
# -----------------------------------------------------------------------

# Remove rows with missing data
df_complete = df.dropna()
print(df_complete.shape) # inspect how many rows were deleted

# Transform the binary target into numerical data using Dictionary
ducks_mapper = {'NO': 0,
    'YES' : 1} 
ducks_target = df_complete['rideducks'].map (ducks_mapper)

# Transform explanatory nominal vars into numerical data using Dictionary
# Use Dictionary to store mapping
# Create new DF

sex_mapper = {'Female': 0, 'Male': 1}
sex = df_complete['sex'].map(sex_mapper)
#print (sex) # inspect sex transformation

age_mapper = {'LT 25' : 1, 
     '25-34' : 2, 
     '35-44' : 3, 
     '45-54' : 4, 
     '55-64' : 5,
     '65+' : 6}
age = df_complete['age'].map(age_mapper)   
#print (age)
     
education_mapper = {'HS Grad or Less':0,
    'Some College': 1,
    'College Grad': 2,
    'Post Grad':3}
education = df_complete['education'].map(education_mapper)    
    
income_mapper = {'Lower Income':0,
    'Middle Income': 1,
    'Upper Income': 2 }
income = df_complete['income'].map(income_mapper)        

planning_mapper = { 'One Month or More Ago': 0,
    'This Month': 1,
    'This Week': 2}
planning = df_complete['planning'].map(planning_mapper)    
    
kids_mapper = {'No kids': 0,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5+': 5}
kids = df_complete['nchildren'].map(kids_mapper)    

nights_mapper = { '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,    
    '4+': 4}
nights = df_complete['nnights'].map(nights_mapper) 

adults_mapper = { '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,    
    '5+': 5}
adults = df_complete['nadults'].map(adults_mapper)    

region_mapper = { 'Chicago': 0,
    'Madison': 1,
    'Milwaukee':2,
    'Minneapolis/StPaul':3,
    'Other Wisconsin': 4,
    'Other': 5 }
region = df_complete['region'].map(region_mapper)    
        
# gather all explanatory variables into a numpy array 
# here we use .T to obtain the transpose for the structure we want
x = np.array([np.array(nights), np.array(adults), np.array(kids),
    np.array(planning), np.array(sex), np.array(age),
    np.array(education), np.array(income), np.array(region)]).T
print(x.shape)  # check the structure of the array of explanatory variables
print(x[0:10,])  # examine the first 10 rows of data

# ---------------------------------------------
# build a simple tree classifier for these data
#----------------------------------------------

# define modeling method with random number seed for reproducibility
from sklearn import tree 
model = tree.DecisionTreeClassifier(random_state = 9999)
my_tree = model.fit(x, ducks_target)  # defines tree classifier object

# use tab completion to see methods available for this object
# my_tree.<tab>
# use my_tree? to obtain information about the object

# multi-fold cross-validation with ten folds
from sklearn.cross_validation import cross_val_score
cv_results = cross_val_score(model, x, ducks_target, cv=10)
round(cv_results.mean(),3)  # cross-validation average proportion correct 
print (cv_results)

# lets see what the fitted tree looks like
from sklearn.externals.six import StringIO  
with open('ducks.dot', 'w') as f:
    f = tree.export_graphviz(my_tree, out_file=f)




















