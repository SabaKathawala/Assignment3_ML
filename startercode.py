#From the console, run the following
#pip is a package management system used to install and manage software packages written in Python
#pip install numpy
#pip install scipy
#pip install scikit-learn
#pip install matplotlib

import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as mp
from pylab import show
from sklearn.model_selection import KFold, cross_val_score

#Load data from a text file.
data = np.loadtxt("data.csv")

#shuffle the data and select training and test data
np.random.seed(100)
np.random.shuffle(data)

features = []
digits = []


for row in data:
    if(row[0]==1 or row[0]==5):
        features.append(row[1:])
        digits.append(str(row[0]))

#select the proportion of data to use for training
numTrain = int(len(features)*.2)

trainFeatures = features[:numTrain]
testFeatures = features[numTrain:]
trainDigits = digits[:numTrain]
testDigits = digits[numTrain:]

#create the model
#https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html

'''X = []
Y = []
simpleTrain = []
colors = []
for index in range(len(trainFeatures)):
    X.append(trainFeatures[index][72])
    Y.append(trainFeatures[index][88])
    simpleTrain.append([trainFeatures[index][72],trainFeatures[index][88]])
    if(trainDigits[index]=="1.0"):
        colors.append("b")
    else:
        colors.append("r")
'''
#calculating new features: mean intensity(X_2D) and intensity variation(Y_2D)
X_2D = []
Y_2D = []
simpleTrain_2D = []
colors_2D = []

for index in range(len(trainFeatures)):
    mean_intensity = np.mean(trainFeatures[index])
    intensity_variation = np.var(trainFeatures[index])

    X_2D.append(mean_intensity)
    Y_2D.append(intensity_variation)

    if (trainDigits[index] == "1.0"):
        colors_2D.append("r")
    else:
        colors_2D.append("b")


minX = np.min(X_2D)
maxX = np.max(X_2D)
minY = np.min(Y_2D)
maxY = np.max(Y_2D)
diffX = maxX - minX
diffY = maxY - minY

#normalizing data

X_2D = [(2 * (x - minX) / diffX) - 1 for x in X_2D]
Y_2D = [(2 * (y - minY) / diffY) - 1 for y in Y_2D]

for i in range(len(X_2D)):
    simpleTrain_2D.append([X_2D[i], Y_2D[i]])

# https://matplotlib.org/api/_as_gen/matplotlib.pyplot.scatter.html
# this just shows the points
mp.xlabel("Mean Intensity")
mp.ylabel("Intensity Variation")

#plotting graph for Fig1.1
mp.scatter(X_2D, Y_2D, s=2, c=colors_2D)
show()

xPred = []
yPred = []
cPred = []
model = KNeighborsClassifier(n_neighbors=3, metric='euclidean')
model.fit(simpleTrain_2D, trainDigits)
for xP in range(-100,100):
    xP = xP/100.0
    for yP in range(-100,100):
        yP = yP/100.0
        xPred.append(xP)
        yPred.append(yP)
        if(model.predict([[xP,yP]])=="1.0"):
            cPred.append("r")
        else:
            cPred.append("b")

#plotting graph for Fig1.2
mp.scatter(xPred,yPred,s=3,c=cPred,alpha=.2)
show()

X_new = []
Y_new = []
simpleTrain_new = []
colors_new = []

for index in range(len(trainFeatures)):
    simpleTrain_new.append(trainFeatures[index])
    if(trainDigits[index]=="1.0"):
        colors_new.append("r")
    else:
        colors_new.append("b")


#https://matplotlib.org/api/_as_gen/matplotlib.pyplot.scatter.html
#this just shows the points


#10FCV for 2D and 256D
k_fold = KFold(n_splits=10, random_state=None, shuffle=True)
metrics = ['euclidean','manhattan','chebyshev']
for metric in metrics:
    model = KNeighborsClassifier(n_neighbors=1, metric=metric)
    model.fit(simpleTrain_new,trainDigits)
    accuracy = cross_val_score(model, simpleTrain_new, trainDigits, cv=k_fold, n_jobs=1)
    error = 1 - accuracy
    print(error)

for metric in metrics:
    model = KNeighborsClassifier(n_neighbors=1, metric=metric)
    model.fit(simpleTrain_2D, trainDigits)
    accuracy = cross_val_score(model, simpleTrain_2D, trainDigits, cv=k_fold, n_jobs=1)
    error = 1-accuracy
    print(error)

k = []
Ecv = []

#odd K calulations 256 D
for i in range(1,50,2):
    model = KNeighborsClassifier(n_neighbors=i, metric='euclidean')
    model.fit(simpleTrain_new, trainDigits)
    accuracy = cross_val_score(model, simpleTrain_new, trainDigits, cv=k_fold, n_jobs=1)
    error = 1 - accuracy
    Ecv.append(np.mean(error))
    k.append(i)

mp.plot(k,Ecv)
show()

k = []
Ecv = []
#odd K calulations 2 D
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





