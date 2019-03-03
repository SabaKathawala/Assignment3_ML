import numpy as np

def fetch_data(data_file):
    # Load data from a text file.
    data = np.loadtxt(data_file)

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

    return trainFeatures, testFeatures, trainDigits, testDigits