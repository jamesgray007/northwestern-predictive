# ----------------------------------------------------
# Random forests plus snippets of code from chapter 8
# ----------------------------------------------------
import pandas as pd  # DataFrame structure and operations
import patsy  # translate model specification into design matrices
from sklearn.ensemble import RandomForestClassifier  # random forests

# Evaluating Predictive Accuracy of a Binary Classifier (Python)
# This utility assumes confusion matrix input cmat is a pandas
# DataFrame created using the crosstab method with the predicted 
# class entered first and the observed class entered second.
def evaluate_classifier(cmat):
    if (str(type(cmat)) != "<class 'pandas.core.frame.DataFrame'>"):
        print('\nError: evaluate_classifier needs pandas DataFrame input\n')
        return(None)
    else:
        a = float(cmat.ix[0,0])
        b = float(cmat.ix[0,1])
        c = float(cmat.ix[1,0]) 
        d = float(cmat.ix[1,1])
        n = a + b + c + d
        predictive_accuracy = (a + d)/n
        true_positive_rate = a / (a + c)
        false_positive_rate = b / (b + d)
        precision = a / (a + b)
        specificity = 1 - false_positive_rate   
        expected_accuracy = ((a + b)*(a + c) + (b + d)*(c + b))/(n * n)
        kappa = (predictive_accuracy - expected_accuracy)\
           /(1 - expected_accuracy)
        return(a, b, c, d, true_positive_rate, false_positive_rate,\
            predictive_accuracy, precision, specificity,\
            expected_accuracy, kappa)

# model specification in R-like formula syntax
# the class is y and the other variables are explanatory variables
text_classification_model = 'y ~  beautiful +\
    best + better + classic + enjoy + enough +\
    entertaining + excellent +\
    fans +  fun + good + great + interesting + like +\
    love +  nice + perfect + pretty + right +\
    top + well + won + wonderful + work + worth +\
    bad + boring + creepy + dark + dead+\
    death + evil + fear + funny + hard + kill +\
    killed + lack + lost + mystery +\
    plot + poor + problem + sad + scary +\
    slow + terrible + waste + worst + wrong'

# patsy package helps to construct the y and x as needed for sklearn
# fit random forest model to the training data
y,x = patsy.dmatrices(text_classification_model,\
    train_data_frame, return_type = 'dataframe')    

# now we specify the nature of the random forest to be constructed
# for reproducibility set random number seed with random_state
my_rf_model = RandomForestClassifier(n_estimators = 10, random_state = 9999)

# then we fit this kind of random forest to the training data
my_rf_model_fit = my_rf_model.fit(x, np.ravel(y))
train_data_frame['pred_rf_binary'] = my_rf_model_fit.predict(x)
train_data_frame['pred_rf'] =\
    train_data_frame['pred_rf_binary'].map(binary_to_thumbsupdown)

# pandas crosstab function is useful for getting the confusion matrix
# construct the confusion matrix for input to evaluate_classifier
cmat = pd.crosstab(train_data_frame['pred_rf'],\
    train_data_frame['thumbsupdown'])

# here we employ the user-defined function to evaluate the classifier
print('\n Random Forest Training Set Performance\n',\
    'Percentage of Reviews Correctly Classified:',\
    100 * round(evaluate_classifier(cmat)[4], 3),'\n')

# use the model developed on the training set to predict
# thumbs up or down reviews in the test set 
# assume that y is not known... only x obtained from patsy
y,x = patsy.dmatrices(text_classification_model,\
        test_data_frame, return_type = 'dataframe') 
y = []  # ignore known thumbs up/down from test set... 
test_data_frame['pred_rf_binary'] = my_rf_model_fit.predict(x)
test_data_frame['pred_rf'] =\
    test_data_frame['pred_rf_binary'].map(binary_to_thumbsupdown)

# construct the confusion matrix for input to evaluate_classifier
cmat = pd.crosstab(test_data_frame['pred_rf'],\
    test_data_frame['thumbsupdown'])

print('\n Random Forest Test Set Performance\n',\
    'Percentage of Reviews Correctly Classified:',\
    100 * round(evaluate_classifier(cmat)[4], 3),'\n')