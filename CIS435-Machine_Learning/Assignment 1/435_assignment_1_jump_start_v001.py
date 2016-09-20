                                     # Assignment 1: Python Jump-Start Program
# 
# We show how to work with a variety of data structures in Python, 
# and in the process begin an analysis of the Wisconsin Dells case study data.
# For purposes of demonstration, we will focus on the Wisconsin Dells visitors 
# who go bungeejumping.

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
# Focus on the Wisconsin Dells visitors who go bungeejumping
# ----------------------------------------------------------

# to see the data we need to do a little work due to the large number of columns
# documentation for what we are doing here is available at
# http://pandas.pydata.org/pandas-docs/stable/basics.html?highlight=set_option
pd.set_option('display.max_columns', 11)  # to allow at most 11 columns of data output

# the Wisconsin Dells demographic data are provided in the first ten columns
# let's select those columns along with the column for bungeejumping, 
# this will give us 11 columns of data for our analysis
# let's use df as a shorthand for our working data frame
# a Python list is used to specify the columns of interest

df = pd.DataFrame(wi_dells_data, 
    columns = ["id", "nnights", "nadults", "nchildren", "planning", 
    "sex", "age", "education", "income", "region", "bungeejumping"])
    
print("\nContents of the working data frame df---------------")
# examine the structure of this DataFrame object
print(df)    
    
# print the first five rows of the DataFrame7zx
print(pd.DataFrame.head(df))  # note NaN values for missing data

# cross-tabulation for sex of respondent and engaging in bungeejumping
print(pd.crosstab(df.sex, df.bungeejumping))



















