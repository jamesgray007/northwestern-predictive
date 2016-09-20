# a few useful modules for our work with the Wisconsin Dells case
import pandas as pd  # pandas for data frame operations
import numpy as np  # arrays and efficient calculation 
import sklearn as sk  # machine learning tools

# IPython magic command %whos shows available objects... modules
# IPython magic command %run runs an entire script/program
# use the object name followed by ? to get information about an object
# use tab completion to see available methods: <tab>
# see display options for pandas with  pd.options.display.<tab>
# set maximum number of rows to twenty  
pd.options.display.max_rows = 20

wi_dells = pd.read_csv('wisconsin_dells.csv')
print(wi_dells.shape)  # check the structure of the data frame

# let's work with a subset of the data columns for now
df = pd.DataFrame(wi_dells, 
    columns = ['sex', 'age', 'nnights', 'nadults', 'nchildren', 'gambling'])
print(df.head)  # examine the first 60 lines of the data frame
print(df.shape)  # check the structure of the data frame

# remove records with missing data
df_complete = df.dropna()
print(df_complete.shape)

# ---------------------------------------------
# data munging to prepare data for scikit-learn
#----------------------------------------------
# note that scikit-learn is built upon numpy
# and numpy works with numeric arrays of data

# use dictionary object for mapping the response/target variable
activity_to_binary = {'NO' : -1, 'YES' : 1}
y = df_complete['gambling'].map(activity_to_binary)
print(y[0:10])  # examine the first 10 rows of data

# use dictionary object for mapping the sex variable
sex_to_binary = {'Female' : 0, 'Male' : 1}
sex = df_complete['sex'].map(sex_to_binary)
print(sex[0:10])  # examine the first 10 rows of data

# use dictionary object for mapping the age variable
age_to_ordinal = {'LT 25' : 1, 
     '25-34' : 2, 
     '35-44' : 3, 
     '45-54' : 4, 
     '55-64' : 5,
     '65+' : 6}
age = df_complete['age'].map(age_to_ordinal)
print(age[0:10])  # examine the first 10 rows of data

# gather the explanatory variables (sex and age) into a numpy array 
# here we use .T to obtain the transpose for the structure we want
x = np.array([np.array(sex), np.array(age)]).T
print(x.shape)  # check the structure of the array of explanatory variables
print(x[0:10,])  # examine the first 10 rows of data

# ---------------------------------------------
# build a simple tree classifier for these data
#----------------------------------------------

# define modeling method with random number seed for reproducibility
from sklearn import tree 
model = tree.DecisionTreeClassifier(random_state = 9999)
my_tree = model.fit(x, y)  # defines tree classifier object

# use tab completion to see methods available for this object
# my_tree.<tab>
# use my_tree? to obtain information about the object

# multi-fold cross-validation with ten folds
from sklearn.cross_validation import cross_val_score
cv_results = cross_val_score(model, x, y, cv=10)
round(cv_results.mean(),3)  # cross-validation average proportion correct 

# lets see what the fitted tree looks like
from sklearn.externals.six import StringIO  
with open('gambling.dot', 'w') as f:
    f = tree.export_graphviz(my_tree, out_file=f)

# lacking a Python-based module for plotting the tree, we will resort 
# downloading an external package from http://www.graphviz.org/
# we install the package and note the location of the icon for the application
# then we drag and drop the .dot output file into the icon for the application
# if all is good, we should get a new window with the tree displayed
