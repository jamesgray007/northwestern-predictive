# Jump-Start for the Bank Marketing Study
# implementing training-and-test regimen

# original source data from http://archive.ics.uci.edu/ml/datasets/Bank+Marketing 

from __future__ import division, print_function
from future_builtins import ascii, filter, hex, map, oct, zip

import sklearn as sk
import sklearn.linear_model as sklm
import sklearn.cross_validation as skcv
import numpy as np  # efficient processing of numerical arrays
import pandas as pd  # pandas for data frame operations
import matplotlib.pyplot as plt  # for plotting ROC curve

# use the full data set after development is complete with the smaller data set
# bank = pd.read_csv('bank-full.csv', sep = ';')  # start with smaller data set

# initial work with the smaller data set
bank = pd.read_csv('bank.csv', sep = ';')  # start with smaller data set
# drop observations with missing data, if any
bank.dropna()

# examine the shape of the DataFrame
print(bank.shape)

# look at the list of column names, note that y is the response
list(bank.columns.values)

# look at the beginning of the DataFrame
bank.head()

# define response variable of use in the model
convert_to_binary = {'no' : 0, 'yes' : 1}
y = bank['y'].map(convert_to_binary)

# define binary variable for having credit in default
default = bank['default'].map(convert_to_binary)

# define binary variable for having a personal loan
housing = bank['housing'].map(convert_to_binary)

# define binary variable for having a personal loan
loan = bank['loan'].map(convert_to_binary)

# use average yearly balance in euros as explanatory variable
balance = bank['balance']

# number of previous contacts
previous = bank['previous']

# define binary indicator variables using pandas get_dummies method
# need one fewer binary indicator variables than number of categories
dummies = pd.get_dummies(bank['job'], prefix = 'job')
bank = bank.join(dummies)

# look at the list of column names with dummies added
list(bank.columns.values)

# arbitrary definition of three classes of jobs where known
job_white_collar = bank['job_admin.'] + bank['job_management'] + bank['job_entrepreneur'] + bank['job_self-employed']
job_blue_collar = bank['job_blue-collar'] + bank['job_services'] + bank['job_technician'] + bank['job_housemaid']
job_other = bank['job_student'] + bank['job_retired'] + bank['job_unemployed'] 

# gather selected explanatory variables into a numpy array 
# here we use .T to obtain the transpose for the structure we want
x = np.array([np.array(default), np.array(housing), np.array(loan), 
    np.array(balance), np.array(previous), 
    np.array(job_white_collar),
    np.array(job_blue_collar),
    np.array(job_other)]).T

# set up data for training-test regimen
x_train, x_test, y_train, y_test = skcv.train_test_split(x, y, test_size=0.3, random_state = 9999)

# fit a logistic regression model to the training data
# note differences with and without class_weight settings
# by using class_weight = 'auto' argument in LogisticRegression
logreg = sklm.LogisticRegression()
my_model_fit = logreg.fit(x_train, y_train)

# predicted class in training set only
y_train_pred = my_model_fit.predict(x_train)
print('Confusion matrix for training set')
print(sk.metrics.confusion_matrix(y_train, y_train_pred))
print('Predictive accuracy in training set:',round(sk.metrics.accuracy_score(y_train, y_train_pred), 3))

# compute ROC curve and area under the ROC curve for the training data
probs = my_model_fit.predict_proba(x_train)
false_positive, true_positive, thresholds = sk.metrics.roc_curve(y_train, probs[:, 1])
roc_auc = sk.metrics.auc(false_positive, true_positive)
print('Area under the ROC curve for training set:', round(roc_auc,3))

# Plot ROC curve to IPython shell and to external file
plt.clf()
plt.plot(false_positive, true_positive, label='ROC Curve (area = %0.3f)' % roc_auc)
plt.plot([0, 1], [0, 1], 'k--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve for Logistic Regression (Training Set)')
plt.legend(loc="lower right")
plt.savefig('plot_train_roc.pdf')

# predicted class in test set
y_test_pred = my_model_fit.predict(x_test)
print('Confusion matrix for test set')
print(sk.metrics.confusion_matrix(y_test, y_test_pred))
print('Predictive accuracy in test set:',round(sk.metrics.accuracy_score(y_test, y_test_pred), 3))

# compute ROC curve and area under the ROC curve for the testing data
probs = my_model_fit.predict_proba(x_test)
false_positive, true_positive, thresholds = sk.metrics.roc_curve(y_test, probs[:, 1])
roc_auc = sk.metrics.auc(false_positive, true_positive)
print('Area under the ROC curve for test set:', round(roc_auc,3))

# Plot ROC curve to IPython shell and to external file
plt.clf()
plt.plot(false_positive, true_positive, label='ROC Curve (area = %0.3f)' % roc_auc)
plt.plot([0, 1], [0, 1], 'k--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve for Logistic Regression (Test Set)')
plt.legend(loc="lower right")
plt.savefig('plot_test_roc.pdf')
 
 