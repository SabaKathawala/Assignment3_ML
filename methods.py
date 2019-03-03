import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plot
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

#plot parameters
colors = ['red', 'blue']
s = 3
alpha = 0.8

#create kPCA model
from sklearn.decomposition import KernelPCA
transformer = KernelPCA(n_components=2, kernel='poly')
X_transformed = transformer.fit_transform(trainFeatures)
#print X_transformed

plot.figure()
for i in range(0, len(X_transformed)):
    plot.scatter(X_transformed[i, 0], X_transformed[i, 1],
                 color=colors[0 if trainDigits[i] == "1.0" else 1], alpha=alpha, s=s)

# plot.legend(loc='best', shadow=False, scatterpoints=1)
# plot.title('kPCA of Digits Dataset')
# show()
# plot.close()

X_feature1 = []
X_feature2 = []
var = 0
for i in range(0, len(X_transformed)):
   var +=  (X_transformed[i,0] + X_transformed[i,1]) / float(np.var(trainFeatures[i]))

print float(var)/len(X_transformed)
#Percentage of variance explained for each components
#print('explained variance ratio (first two components): %s'
 #     % str(transformer.explained_variance_ratio_))


#print np.var(X_transformed)
# explained_variance = np.var(X_transformed, axis=0)
# explained_variance_ratio = explained_variance / np.sum(explained_variance)
#
# print explained_variance