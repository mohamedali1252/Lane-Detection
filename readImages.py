import glob
import cv2
import matplotlib.pyplot as plt
import numpy as np
from skimage.feature import hog
from pickle import dump
import pandas as pd

# Read all images in the current directory
def loadImages():
    cars = glob.glob("Data/vehicles/GTI_Far/*.png")
    cars += glob.glob("Data/vehicles/GTI_Left/*.png")
    cars += glob.glob("Data/vehicles/GTI_MiddleClose/*.png")
    cars += glob.glob("Data/vehicles/GTI_Right/*.png")
    cars += glob.glob("Data/vehicles/KITTI_extracted/*.png")
    notCars = glob.glob("Data/non-vehicles/extras/*.png")
    notCars += glob.glob("Data/non-vehicles/GTI/*.png")
    return cars, notCars

def calculateHog(img, orient = 9, pix_per_cell = 8, cell_per_block = 3, vis = False, feature_vec = True):
    output = hog(img, orientations=orient, pixels_per_cell=(pix_per_cell, pix_per_cell), \
                   cells_per_block=(cell_per_block, cell_per_block), transform_sqrt=False, \
                   visualize=vis, feature_vector=feature_vec, block_norm="L2-Hys")
    if vis:
        features, hog_image = output
        return features, hog_image
    return output

def channels_3_Hog(img):
    features = []
    for channel in range(img.shape[2]):
        features.extend(calculateHog(img[:,:,channel])) 
    return features

def showImage(img):
    cmap = 'gray'
    try:
        if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            cmap = None
        plt.imshow(img, cmap=cmap)
        plt.show()
    except:
        print("Error: invalid image")

def generateDataset(lst):
    dataset = []
    for element in lst:
        img = cv2.imread(element)
        dataset.append(channels_3_Hog(img))
    return dataset

cars, notCars = loadImages()
# for i in range(4):
#     if i == 0:
#         dataset = generateDataset(notCars[:2000])
#         dump(dataset, open('dnc0-2.pkl', 'wb'))
#         break
#     if i == 1:
#         dataset = generateDataset(notCars[2000:4000])
#         dump(dataset, open('dnc2-4.pkl', 'wb'))
#     if i == 2:
#         dataset = generateDataset(notCars[4000:6000])
#         dump(dataset, open('dnc4-6.pkl', 'wb'))
#     if i == 3:
#         dataset = generateDataset(notCars[6000:])
#         dump(dataset, open('dnc6-8.pkl', 'wb'))
# columns = [i for i in range(dataset.shape[1]-1)]
# columns.append('car')
# dataset.columns = columns    
# print("Number of car images:", len(cars))
# print("Number of not car images:", len(notCars))
# print(dataset)

# 0 => gray scale, 1 => color
# img = cv2.imread(cars[0])
# features, img = calculateHog(img, vis = True)
# features = calculateHog(img)
# features = channels_3_Hog(img)
# features = np.append(features, 1)
# print(features)
# print(features.shape)

# # showImage(img)
# print(len(features))

# print(len(cars))
# print(dataset)
# print(dataset.shape)