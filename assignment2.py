#From the console, run the following
#pip is a package management system used to install and manage software packages written in Python
#pip install numpy
#pip install scipy
#pip install scikit-learn
#pip install matplotlib

import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plot
from pylab import show
from sklearn.model_selection import KFold, cross_val_score
from sklearn.decomposition import KernelPCA


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

X = []
Y = []
simpleTrain = []
colors = []
for index in range(len(trainFeatures)):
    X.append(trainFeatures[index])
    Y.append(trainDigits[index])

#create kPCA model
def kPCA(X):
    transformer = KernelPCA(n_components=2, kernel='poly')
    X_transformed = transformer.fit_transform(X)
    print X_transformed
    return X_transformed


X_transformed = kPCA(X)

plot.figure()
colors = ['red', 'blue']
lineWidth = 1
alpha = 0.8

for i in range(0, 256):
    plot.scatter(X_transformed[i, 0], X_transformed[i, 1],
                 color=colors[0 if Y[i] == "1.0" else 1], alpha=alpha, linewidths=lineWidth)

plot.legend(loc='best', shadow=False, scatterpoints=1)
plot.title('kPCA of Digits Dataset')
show()
plot._imsave()
plot.close()


# Percentage of variance explained for each components
#print('explained variance ratio (first two components): %s'
 #     % str(transformer.explained_variance_ratio_))


#print np.var(X_transformed)
explained_variance = np.var(X_transformed, axis=0)
explained_variance_ratio = explained_variance / np.sum(explained_variance)

print explained_variance

X_2D = []
Y_2D = []

test_X = []
test_Y = []
simpleTrain_2D = []
colors_2D = []
colors_test = []

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

for index in range(len(testFeatures)):
    test_mean = np.mean(testFeatures[index])
    test_intensity = np.var(testFeatures[index])

    test_X.append(test_mean)
    test_Y.append(test_intensity)

    if (testDigits[index] == "1.0"):
        colors_test.append("r")
    else:
        colors_test.append("b")

minX = np.min(test_X)
maxX = np.max(test_X)
minY = np.min(test_Y)
maxY = np.max(test_Y)
diffX = maxX - minX
test_X = [(2 * (x - minX) / diffX) - 1 for x in test_X]
test_Y = [(2 * (y - minY) / diffY) - 1 for y in test_Y]

for i in range(len(X_2D)):
    simpleTrain_2D.append([X_2D[i], Y_2D[i]])

#print np.var(simpleTrain_2D)

'''lda = LinearDiscriminantAnalysis(n_components=2)
X_r2 = lda.fit(X, Y).transform(X)
print(X_r2)

for i in range(0, 256):
    plt.scatter(X_r2[i,0], X_r2[i,1], color=colors[0 if Y[i]== "1.0" else 1], alpha=.8, linewidths=linewidth)
plt.legend(loc='best', shadow=False, scatterpoints=1)
plt.title('LDA of Digits dataset')

show()'''

from sklearn.linear_model import LogisticRegression

'''logisticRegClassifier = LogisticRegression(C=50.0).fit(simpleTrain_2D, Y)
xPred = []
yPred = []
cPred = []
success = 0
fail = 0
for xP, yP, td in zip(test_X, test_Y, testDigits):
    if(logisticRegClassifier.predict([[xP,yP]])==td):
        cPred.append("r")
        success+=1
    else:
        cPred.append("b")
        fail += 1
print success
print fail

#plotting graph for Fig1.2
plt.scatter(test_X,test_Y,c=colors_test,alpha=.2)
plt.scatter(test_X,test_Y,c=cPred,alpha=.2)
show()'''



c = 0.01
while(c <= 2.1):
    logisticRegClassifier = LogisticRegression(C=c).fit(simpleTrain_2D, Y)
    xPred = []
    yPred = []
    cPred = []
    for xP in range(-100,100):
        xP = xP/100.0
        for yP in range(-100,100):
            yP = yP/100.0
            xPred.append(xP)
            yPred.append(yP)
            if(logisticRegClassifier.predict([[xP,yP]])=="1.0"):
                cPred.append("r")
            else:
                cPred.append("b")

    #plotting graph for Fig1.2
    plot.scatter(xPred,yPred,s=3,c=cPred,alpha=.2)
    show()
    print c
    c += 0.25

# kahani SVM ki - hosh posh

from sklearn.svm import SVC
from sklearn.model_selection import KFold, cross_val_score

k_fold = KFold(n_splits=10, random_state=None, shuffle=True)
c = 0.01
for i in range(1, 20, 1):
    clf = SVC(C=c)
    clf.fit(simpleTrain_2D, Y)
    accuracy = cross_val_score(clf, simpleTrain_2D, Y, cv=k_fold, n_jobs=1)
    mean = np.mean(accuracy)
    print c, mean, np.log10(c)
    c+=0.05
c = 1
best_c = -1
best_mean = -1
for i in range(1, 101, 1):
    clf = SVC(C=c)
    clf.fit(simpleTrain_2D, Y)
    accuracy = cross_val_score(clf, simpleTrain_2D, Y, cv=k_fold, n_jobs=1)
    mean = np.mean(accuracy)
    print c, mean, np.log10(c)
    if (mean > best_mean):
        best_mean = mean
        best_c = c
    c+=1

print 'best c ', best_c

c = 20 # is the value to use aage se

# clf = SVC(C=c)
# clf.fit(simpleTrain_2D, Y)
# xPred = []
# yPred = []
# cPred = []
# for xP in range(-100,100):
#     xP = xP/100.0
#     for yP in range(-100,100):
#         yP = yP/100.0
#         xPred.append(xP)
#         yPred.append(yP)
#         if(clf.predict([[xP,yP]])=="1.0"):
#             cPred.append("r")
#         else:
#             cPred.append("b")
# # plotting graph for Fig1.2
# plt.scatter(xPred,yPred,s=3,c=cPred,alpha=.2)
# show()

# read - https://stats.stackexchange.com/questions/35276/svm-overfitting-curse-of-dimensionality

degrees = [2,5,10,20]
for d in degrees:
    clf = SVC(C=c, degree=d)
    clf.fit(simpleTrain_2D, Y)
    accuracy = cross_val_score(clf, simpleTrain_2D, Y, cv=k_fold, n_jobs=1)
    mean = np.mean(accuracy)
    print d, mean
    xPred = []
    yPred = []
    cPred = []
    for xP in range(-100,100):
        xP = xP/100.0
        for yP in range(-100,100):
            yP = yP/100.0
            xPred.append(xP)
            yPred.append(yP)
            if(clf.predict([[xP,yP]])=="1.0"):
                cPred.append("r")
            else:
                cPred.append("b")
    # plotting graph for Fig1.2
    plot.scatter(xPred, yPred, s=3, c=cPred, alpha=.2)
    show()


# 96 is the best c