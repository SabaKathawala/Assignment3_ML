# From the console, run the following
# pip is a package management system used to install and manage software packages written in Python
# pip install numpy
# pip install scipy
# pip install scikit-learn
# pip install matplotlib

import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as mp
from pylab import show
from sklearn.model_selection import KFold, cross_val_score
from sklearn.model_selection import validation_curve

# Load data from a text file.
data = np.loadtxt("data.csv")

# shuffle the data and select training and test data
np.random.seed(100)
np.random.shuffle(data)

features = []
digits = []

for row in data:
    if (row[0] == 1 or row[0] == 5):
        features.append(row[1:])
        digits.append(str(row[0]))

# select the proportion of data to use for training
numTrain = int(len(features) * .2)

trainFeatures = features[:numTrain]
testFeatures = features[numTrain:]
trainDigits = digits[:numTrain]
testDigits = digits[numTrain:]

# create the model
# https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html


'''X = []
Y = []
simpleTrain = []
colors = []
for index in range(len(trainFeatures)):
    X.append(trainFeatures[index][72])
    Y.append(trainFeatures[index][88])
    simpleTrain.append([trainFeatures[index][72], trainFeatures[index][88]])
    if (trainDigits[index] == "1.0"):
        colors.append("b")
    else:
        colors.append("r")
'''



metrics = ['euclidean','manhattan','chebyshev']
#shuffle data when cross validating
#calculating 10-fold cross validation error
k_fold = KFold(n_splits=10, random_state=None, shuffle=True)


model = KNeighborsClassifier(n_neighbors=1, metric='euclidean')
model.fit(simpleTrain_2D, trainDigits)

k = []
Ecv = []
for i in range(1, 50, 2):
    model = KNeighborsClassifier(n_neighbors=i, metric='euclidean')
    model.fit(simpleTrain_2D,trainDigits)
    k_fold = KFold(n_splits=10, random_state=None, shuffle=True)
    accuracy = cross_val_score(model, simpleTrain_2D, trainDigits, cv=k_fold, n_jobs=1)
    error = 1 - accuracy
    # print(error)
    print('Error :', np.mean(error))
    Ecv.append(np.mean(error))
    k.append(i)

mp.plot(k,Ecv)
show()
