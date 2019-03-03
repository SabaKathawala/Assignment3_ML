import numpy as np
import math

X=np.array(([0,0,1],[0,1,1],[1,0,1],[1,1,1]), dtype=float)
y=np.array(([0],[1],[1],[0]), dtype=float)




def sigmoid(x):
    return 1 / (1 + math.exp(-x))

# z(1-z)
def sigmoid_derivative(z):
    return z * (1-z)


class NeuralNetwork:
    learningRate = 1
    numLayers = 1
    numNeurons = 1
    maxIterations = 1

    def __init__(self, x, y, learningRate, maxIterations, numLayers, numNeurons):
        self.input      = x
        self.weights1   = np.random.rand(self.input.shape[1],4)
        self.weights2   = np.random.rand(4,1)
        self.y          = y
        self.output     = np.zeros(y.shape)

        #additional pieces
        self.learningRate = learningRate
        self.numLayers = numLayers
        self.numNeurons = numNeurons
        self.maxIterations = maxIterations

    def feedforward(self):

        self.layer1 = sigmoid(np.dot(self.input, self.weights1))        #dot product weights and input
        self.layer2 = sigmoid(np.dot(self.layer1, self.weights2))
        self.output = sigmoid(np.dot(self.layer2, self.weights3))

    def backprop(self):
        # application of the chain rule to find derivative of the loss function with respect to weights2 and weights1
        d_weights2 = np.dot(self.layer1.T, (2 * (self.y - self.output) * sigmoid_derivative(self.output)))
        d_weights1 = np.dot(self.input.T, (np.dot(2 * (self.y - self.output) * sigmoid_derivative(self.output),
                                                  self.weights2.T) * sigmoid_derivative(self.layer1)))

        # update the weights with the derivative (slope) of the loss function
        self.weights1 += d_weights1
        self.weights2 += d_weights2


np = NeuralNetwork(X, y)