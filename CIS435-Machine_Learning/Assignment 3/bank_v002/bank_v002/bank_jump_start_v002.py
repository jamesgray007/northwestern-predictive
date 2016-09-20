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

# gather these five explanatory variables into a numpy array 
# here we use .T to obtain the transpose for the structure we want
x = np.array([np.array(default), np.array(housing), np.array(loan), 
    np.array(balance), np.array(previous)]).T

# fit a logistic regression model 
# note differences with and without class_weight settings
# by using class_weight = 'auto' argument in LogisticRegression
logreg = sklm.LogisticRegression(C=1e5)
my_model_fit = logreg.fit(x, y)

# predicted class in training data only
y_pred = my_model_fit.predict(x)
print('Confusion matrix for training set')
print(sk.metrics.confusion_matrix(y, y_pred))
print('Predictive accuracy in training set:',round(sk.metrics.accuracy_score(y, y_pred), 3))

# multi-fold cross-validation with 5 folds
cv_results = sk.cross_validation.cross_val_score(logreg, x, y, cv=5)
print('Cross-validation average accuracy:', round(cv_results.mean(),3))  

# compute ROC curve and area under the ROC curve
probs = my_model_fit.predict_proba(x)
false_positive, true_positive, thresholds = sk.metrics.roc_curve(y, probs[:, 1])
roc_auc = sk.metrics.auc(false_positive, true_positive)
print('Area under the ROC curve:', round(roc_auc,3))

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
plt.savefig('plot_roc.pdf')

 