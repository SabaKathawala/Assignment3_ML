from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import KFold, cross_val_score
import numpy as np

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
    simpleTrain.append([trainFeatures[index][72],trainFeatures[index][88]])
    if(trainDigits[index]=="1.0"):
        colors.append("b")
    else:
        colors.append("r")
'''
# calculating new features: mean intensity(X_2D) and intensity variation(Y_2D)
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

# normalizing data

X_2D = [(2 * (x - minX) / diffX) - 1 for x in X_2D]
Y_2D = [(2 * (y - minY) / diffY) - 1 for y in Y_2D]

for i in range(len(X_2D)):
    simpleTrain_2D.append([X_2D[i], Y_2D[i]])

# loop for 1-5 hidden layers
no_of_layers = 1
min_error = 1
layers = 1
nodes = 2
while no_of_layers <= 5:
    #loop for 2-4 nodes
    no_of_neurons = 2
    while no_of_neurons <= 4:
        hidden_layers = (no_of_neurons,) * no_of_layers
        print hidden_layers
        # mlp = MLPClassifier(hidden_layer_sizes=(100, 100), max_iter=400, alpha=1e-4,
        #                     solver='sgd', verbose=10, tol=1e-4, random_state=1)
        mlp_model = MLPClassifier(activation='logistic', hidden_layer_sizes=hidden_layers, solver='sgd')
        model = mlp_model.fit(simpleTrain_2D, trainDigits)
        k_fold = KFold(n_splits=10, random_state=None, shuffle=True)
        accuracy = cross_val_score(model, simpleTrain_2D, trainDigits, cv=k_fold, n_jobs=1)
        error = 1 - accuracy
        mean = np.mean(error)
        print 'No of layers: ', no_of_layers, ' No of neurons: ', no_of_neurons, ' Cross val error: ', mean
        no_of_neurons += 1
        if min_error > mean:
            layers = no_of_layers
            nodes = no_of_neurons
            min_error = mean

    no_of_layers += 1

print layers, nodes, min_error

import matplotlib.pyplot as plot
from pylab import show

mlp_model = MLPClassifier(activation='logistic', hidden_layer_sizes=(nodes,)*layers, solver='sgd')
model = mlp_model.fit(simpleTrain_2D, trainDigits)
xPred = []
yPred = []
cPred = []
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
# plotting graph for Fig1.2
plot.scatter(xPred, yPred, s=3, c=cPred, alpha=.2)
show()