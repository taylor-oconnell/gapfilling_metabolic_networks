import numpy as np
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.utils import shuffle

"""
    This code utilizes the scikitlearn library to train
    a random forest classifier for use inclassifying new 
    observations/examples.  This is an initial test just
    to get the random forest classifier working and it 
    uses the iris dataset that is included in the sample 
    datasets that come with sklearn.
"""

# Load data
iris = load_iris()
X = iris.data      #feature data matrix
Y = iris.target    #class labels
X, Y = shuffle(X, Y, random_state=0)


# Fit random forest classifier to training data
rf_clf = RandomForestClassifier()
rf_clf = rf_clf.fit(X[:100],Y[:100])


# make predictions on test data
predictions = rf_clf.predict(X[100:])

#Print the predictions and print the actual class labels
print "Predictions:"
print predictions
print "\nActual class labels:"
print Y[100:]


total = len(predictions)
print "\n\ntotal # of predictions: " + str(total)
num_correct = sum(predictions == Y[100:])
print "\n# of correct predictions: " + str(num_correct)
num_incorrect = total - num_correct
print "\n# of incorrect predictions: " + str(num_incorrect)

#Calculate and print out the error rate
error_rate = float(num_incorrect) / float(total)
print "\n% error: " + str(error_rate*100) +"%"









