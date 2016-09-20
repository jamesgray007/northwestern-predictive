# James Gray - Northwestern University CIS435 - Assignment #3 (August 2, 2014)
# Bank Marketing Study

# original source data from http://archive.ics.uci.edu/ml/datasets/Bank+Marketing 

from __future__ import division, print_function
from future_builtins import ascii, filter, hex, map, oct, zip

import sklearn as sk
import sklearn.linear_model as sklm
import numpy as np  # efficient processing of numerical arrays
import pandas as pd  # pandas for data frame operations
import matplotlib.pyplot as plt  # for plotting ROC curve
import sklearn.svm as svm # support vector machine classifier
import sklearn.naive_bayes as nb # naive bayes classifier
  
# use the full data set after development is complete with the smaller data set
# bank = pd.read_csv('bank-full.csv', sep = ';')  # start with smaller data set

# ==================================================================================
# data set predictors
# ==================================================================================

# 1 - age: numeric
# 2 - job : type of job (categorical: 'admin.','blue-collar','entrepreneur','
#    housemaid','management','retired','self-employed','services','student',
#    'technician','unemployed','unknown')
# 3 - marital : marital status (categorical: 'divorced','married','single','unknown'; 
#    note: 'divorced' means divorced or widowed)
# 4 - education (categorical: 'basic.4y','basic.6y','basic.9y','high.school','
#    illiterate','professional.course','university.degree','unknown')
# 5 - default: has credit in default? (categorical: 'no','yes','unknown')
# 6 - balance: loan balance
# 7 - housing: has housing loan? (categorical: 'no','yes','unknown')
# 8 - loan: has personal loan? (categorical: 'no','yes','unknown')
# 9 - contact: contact communication type (categorical: 'cellular','telephone') 
# 10 - day: last contact day of the week (categorical: 'mon','tue','wed','thu','fri')
# 11 - month: last contact month of year (categorical: 'jan', 'feb', 'mar'....)
# 12- duration: last contact duration, in seconds (numeric). Should be removed
# 13 - campaign: number of contacts performed during this campaign and for this client\
#    (numeric, includes last contact)
# 14 - pdays: number of days that passed by after the client was last contacted from 
#    a previous campaign (numeric; 999 means client was not previously contacted)
# 15 - previous: number of contacts performed before this campaign and for this client (numeric)
# 16 - poutcome: outcome of the previous marketing campaign (categorical: 'failure',
#    'nonexistent','success')

# ==================================================================================
# output variable
# 21 - y - has the client subscribed a term deposit? (binary: 'yes','no')
# ==================================================================================

# initial work with the smaller data set
bank = pd.read_csv('bank.csv', sep = ';')  # start with smaller data set
# drop observations with missing data, if any
bank.dropna()

# full data set
bank_full = pd.read_csv('bank-full.csv', sep = ';') 
# drop observations with missing data, if any
bank_full.dropna()

# examine the shape of the DataFrame
print(bank.shape)

# look at the list of column names, note that y is the response
list(bank.columns.values)

# look at the beginning of the DataFrame
print (bank.head())

# ==================================================================================
# Data Preparation - Transform categorical data into dummy/indicator variables
# ==================================================================================

# We will use the Pandas .getdummies function to convert categorical variables
# into dummy/indicator variables

# job, marital, education, default, housing, loan, contact, month, poutcome are
# categorical vars that needs to be converted

for column in ['job', 'marital', 'education', 'default', 'housing', 'loan',
    'contact', 'day', 'month', 'poutcome']:
    # create a new dummmies DataFrame that holds the new dummy columns
    dummies = pd.get_dummies(bank[column],prefix=column)
    # add new dummy columns to original bank DataFrame
    bank[dummies.columns] = dummies
    # remove the original categorical column in the bank DataFrame
    bank = bank.drop(column, axis=1)
    print (bank)
    
# confirm new dummy vars have been added
print (bank.head)

# ==================================================================================
# Data Preparation - Transform "yes" or "no" categorical data into binary
# ==================================================================================

# helper dict function to convert yes and no into binary
convert_to_binary = {'no' : 0, 'yes' : 1}

# define response variable of use in the model
y = bank['y'].map(convert_to_binary)

# 5 - define binary variable for having credit in default
#default = bank['default'].map(convert_to_binary)

# 6 - define binary variable for having a housing loan
#housing = bank['housing'].map(convert_to_binary)

# 7- define binary variable for having a personal loan
#loan = bank['loan'].map(convert_to_binary)

# =================================================================================
# Data Preparation - Discretize continuous data into bins
# =================================================================================

# 1 - age array
age = bank['age']

# Discretize age using quantiles - returns a Categorical object (array of strings)
# but numpy array if labels=False

age_to_bins = pd.qcut(age,4,labels=False)

# Transform binned data into indicator variables (DataFrame)
dummies_age_bins = pd.get_dummies(age_to_bins, prefix='age_q')

# append new Age dummy columns to bank DF
bank[dummies_age_bins.columns] = dummies_age_bins

# use average yearly balance in euros as explanatory variable
balance = bank['balance']

# Discretize Balance using quantiles
balance_to_bins = pd.qcut(balance,4,labels=False)

# Transform binned data into indicator variables (DataFrame)
dummies_balance_bins = pd.get_dummies(balance_to_bins, prefix='bal_q')

# append new balance dummy columns to bank DF
bank[dummies_balance_bins.columns] = dummies_balance_bins

# number of previous contacts
previous = bank['previous']

# Discretize previous contacts using quantiles
#previous_to_bins = pd.qcut(previous,4, labels=False)

# Transform binned data into indicator variables (DataFrame)
#dummies_previous_bins = pd.get_dummies(previous_to_bins, prefix='prev_q')

# ================================================================================
# Data Preparation - Construct final x input array
# ================================================================================

# gather these explanatory variables into a numpy array 
# here we use .T to obtain the transpose for the structure we want
#x = np.array([np.array(default), np.array(housing), np.array(loan), 
#    np.array(balance), np.array(previous)]).T

#x = np.array([np.array(previous)]).T

# Drop columns the numerical colums that have been discretized
drop_columns = ['age','balance','duration', 'campaign', 'pdays', 'previous','y']
bank = bank.drop(drop_columns, axis=1)

x = np.array(bank)
                        
# =============================================================================
# LOGISTIC REGRESSION
# =============================================================================

# fit a logistic regression model 
# note differences with and without class_weight settings
# by using class_weight = 'auto' argument in LogisticRegression
logreg = sklm.LogisticRegression(C=1e5)
my_model_fit = logreg.fit(x, y)

# predicted class in training data only
y_pred = my_model_fit.predict(x)
print('Logistic Confusion matrix for training set')
print(sk.metrics.confusion_matrix(y, y_pred))
print('Logistic Predictive accuracy in training set:',round(sk.metrics.accuracy_score(y, y_pred), 3))

# multi-fold cross-validation with 5 folds
cv_results = sk.cross_validation.cross_val_score(logreg, x, y, cv=5)
print('Logistic Cross-validation average accuracy:', round(cv_results.mean(),3))  

# compute ROC curve and area under the ROC curve
probs = my_model_fit.predict_proba(x)
false_positive, true_positive, thresholds = sk.metrics.roc_curve(y, probs[:, 1])
roc_auc = sk.metrics.auc(false_positive, true_positive)
print('Logistic Area under the ROC curve:', round(roc_auc,3))

# Plot ROC curve to IPython shell and to external file
plt.clf()
plt.plot(false_positive, true_positive, label='ROC Curve (area = %0.3f)' % roc_auc)
plt.plot([0, 1], [0, 1], 'k--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve for Logistic Regression')
plt.legend(loc="lower right")
plt.savefig('plot_rocLR.pdf')

# =============================================================================
# SUPPORT VECTOR MACHINE (SVM)
# =============================================================================

# split data for training and testing regimen
from sklearn.cross_validation import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=0)

# Instantiate the estimator
svmclf = svm.SVC(probability=True)

# Fit the estimator to the data
svm_fit = svmclf.fit(x, y) 

# predict class using training data
y_svmpred = svm_fit.predict (x)

# Compare actual y and prediction in a confusion matrix
print(sk.metrics.confusion_matrix(y, y_svmpred))

# Show accuracy rate
print('SVM Predictive accuracy in training set:',round(sk.metrics.accuracy_score(y, y_svmpred), 3))

# SVM multi-fold cross-validation with 5 folds
svm_cv_results = sk.cross_validation.cross_val_score(svmclf, x, y, cv=5)
print('SVM Cross-validation average accuracy:', round(svm_cv_results.mean(),3)) 

# SVM cross-validation with 5 folds using precision
svm_cv_precision_results = sk.cross_validation.cross_val_score(svmclf, x, y,
    cv=5, scoring='f1')
print ('SVM Cross-validation using Precision:', round(svm_cv_precision_results.mean(),3))

# compute ROC curve and area under the ROC curve
svm_probs = svm_fit.predict_proba(x)
false_positive, true_positive, thresholds = sk.metrics.roc_curve(y, probs[:, 1])
svm_roc_auc = sk.metrics.auc(false_positive, true_positive)
print('SVM Area under the ROC curve:', round(svm_roc_auc,3))

# accuracy = correct labels / total samples
# print "accuracy: ", metrics.accuracy_score (y_test, y_pred)

# precision = true positives / (true positives + false positives)
# This represents the % of labeled class that actually the class 
# print "precision: ", metrics.precision_score (y_test, y_pred)

# recall = true positives / (true positives + false negatives)
# This represents the % of the actual class we are pulling out of the sample
# print "recall: ", metrics.recall_score (y_test, y_pred)

# f1 = precision * recall / (precision + recall) 
# print "f1 score: ", metrics.f1_score (y_test, y_pred)

# Print Classificcation report
# print metrics.classification_report (y_test, y_pred, 
#    target_names = ['reject', 'accept']

# Plot ROC curve to IPython shell and to external file
plt.clf()
plt.plot(false_positive, true_positive, label='ROC Curve (area = %0.3f)' % svm_roc_auc)
plt.plot([0, 1], [0, 1], 'k--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve for SVM')
plt.legend(loc="lower right")
plt.savefig('plot_rocSVM.pdf')
 
