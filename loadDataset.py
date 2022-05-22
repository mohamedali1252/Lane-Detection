from readImages import generateDataset, loadImages
from pickle import load
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC, SVC
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from pickle import dump
import numpy as np


# function to split dataset to train and test data
def splitDataset(cars, notCars, test_size = 0.2):
    y: list = np.hstack((np.ones(len(cars)), np.zeros(len(notCars))))
    x: list = cars
    x.extend(notCars)
    # split dataset into train and test data
    train_data, test_data, train_labels, test_labels = train_test_split(x, y, test_size = test_size)
    return train_data, test_data, train_labels, test_labels

# function to train the model
def trainModel(x_train, y_train):
    # create model
    model = SVC(kernel = 'linear', probability=True)
    # fit model
    model.fit(x_train, y_train)
    # return model
    return model

# function to make predictions
def predict(model, x_test):
    # predict
    y_pred = model.predict(x_test)
    # return predictions
    return y_pred

def getProbability(model, x_test):
    y_pred = model.predict_proba(x_test)
    return y_pred

# function to calculate accuracy
def getAccuracy(y_test, y_pred):
    # calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    # return accuracy
    return accuracy

# function to calculate confusion matrix
def getConfusionMatrix(y_test, y_pred, labels):
    # calculate confusion matrix
    cm = confusion_matrix(y_test, y_pred, labels = labels)
    # return confusion matrix
    return cm

# function to save model
def generateModel(model, file = 'model.pkl'):
    # cars, notCars = loadImages()
    # cars: list = generateDataset(cars)
    # notCars: list = generateDataset(notCars)
    # x_train, x_test, y_train, y_test = splitDataset(cars, notCars)
    # model = trainModel(x_train, y_train)
    # y_pred = predict(model, x_test)
    # print(getAccuracy(y_test, y_pred))
    dump(model, open(file, "wb"))
    print('The model is saved.')
    return None

# generateModel('m1_3Channels.pkl')