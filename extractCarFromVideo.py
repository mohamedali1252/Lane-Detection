import cv2
from pickle import load
from readImages import calculateHog, showImage, channels_3_Hog
from sklearn.svm import SVC
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import label
import time
from loadDataset import getProbability

def checkCarExist(img, model):
    img = cv2.resize(img, (64, 64))
    features = np.array(channels_3_Hog(img)).reshape(1, -1)
    prediction = model.predict(features)
    return prediction[0] == 1
    
def part_image(img, rect):
    [[x, y], [w, h]] = rect
    img1 = img[y:y+h, x:x+w]
    img1 = cv2.resize(img1, (64, 64))
    return img1
    
def traverseImage(img, model: SVC, rect=[[30, 380], [140, 140]], y1=656, ther = 0.9):
    img1 = np.zeros_like(img)
    [[x, y], [w, h]] = rect
    x1 = img1.shape[1]
    rects = []
    while y1 > y+h:
        x = 30
        while x1 > x+w:
            img2 = part_image(img, [[x, y], [w, h]])
            features = np.array(channels_3_Hog(img2)).reshape(1,-1)
            prediction = model.predict_proba(features)
            if prediction[0][1] > ther:
                rects.append([[x, y], [x+w, y+h]])
            x += w//4
        y += h//4
    return img1, rects

def traverseImageMultiScale(img, model, sizes=[(140, 140), (100, 100), (64, 64)], x=30,\
            y=[(380, 665), (380, 665), (380, 665)], background=False, ther=0.9):
    img1 = np.zeros_like(img)
    rects = []
    for i in range(len(sizes)):
        img1, rect = traverseImage(img, model, ((x, y[i][0]), sizes[i]), ther=ther)
        rects.extend(rect)
    if not background:
        img1 = cv2.addWeighted(img, 1, img1, 0.5, 0)
    return img1, rects

def getHeatmap(img, rects):
    heatmap = np.zeros(img.shape[:2]).astype(np.float32)
    for rect in rects:
        [[x, y], [x2, y2]] = rect
        heatmap[y:y2, x:x2] += 1
    return heatmap

def thersholdHeatmap(heatmap, thresh=3):
    heatmap = np.copy(heatmap)
    heatmap[heatmap <= thresh] = 0
    heatmap = np.clip(heatmap, 0, 255)
    return heatmap

def filterSomeRects(img, rects, thershold=3):
    heatmap1 = getHeatmap(img, rects)
    heatmap = thersholdHeatmap(heatmap1, thresh=thershold)
    labels, features = label(heatmap)
    rects = []
    for i in range(1, features+1):
        notZero = (labels == i).nonzero()
        notZero_x = np.array(notZero[1])
        notZero_y = np.array(notZero[0])
        rect = ((np.min(notZero_x), np.min(notZero_y)), (np.max(notZero_x), np.max(notZero_y)))
        rects.append(rect)
    return rects, heatmap1

def applyRects(img, rects):
    img1 = img.copy()
    for rect in rects:
        [[x, y], [x2, y2]] = rect
        cv2.rectangle(img1, (x, y), (x2, y2), (0, 255, 0), 4)
    return img1

'''
def clustring_rects(rects):
    x = []
    y = []
    new_rects = []
    for cluster in rects:
        for rect in cluster:
            x.append(rect[0][0])
            x.append(rect[0][0]+rect[1][0])
            y.append(rect[0][1])
            y.append(rect[0][1]+rect[1][1])
        new_rects.append([[min(x),min(y)],[max(x)-min(x),max(y)-min(y)]])
        
    return new_rects

def unique_elements(rect , rects):
    flag = False
    for i in rects:
        if i[0][0]==rect[0][0] and i[0][1]==rect[0][1]:
            i[1][0] = max([i[1][0],rect[1][0]])
            i[1][1] = max([i[1][1],rect[1][1]])
            flag = True
    if flag == False:
        rects.append(rect)
    return rects

def filter_rects(rects: list, ther = 50):
    new_rects = []
    for i in range(len(rects)):
        try:
            new_rect = [rects[i]]
            for j in range(i+1, len(rects)):
                try:
                    if abs(rects[i][0][0]-rects[j][0][0]) < ther and abs(rects[i][0][1]-rects[j][0][1]) < ther:
                        new_rect.append(rects.pop(j))
                except:
                    continue
            new_rects.append(new_rect)
        except:
            continue
    return new_rects
'''

model: SVC = load(open("model1.pkl", "rb"))
def detect_cars(img):
    global model
    img1, rects = traverseImageMultiScale(img, model, sizes=[[80, 80], [100, 100], [124, 124]], ther=0.3)
    rects,_ = filterSomeRects(img1, rects, thershold=3)
    img1 = applyRects(img1, rects)
    return img1

# img = cv2.imread("test_images/test1.jpg")
# img = detect_cars(img)
# showImage(img)
# img1, rects = traverseImageMultiScale(img, model, sizes=[[80, 80], [100, 100], [124, 124]], ther = 0.3)
# rects, heatmap = filterSomeRects(img1, rects, thershold=3)
# rects = filter_rects(rects,40)
#hm = getHeatmap(img1,rects)
#print(rects)
# plt.imshow(heatmap, cmap="hot")
# plt.show()
# for rect in rects:
#     print(rects)
# rects = clustring_rects(rects)
# print('-----------------------')
# for rect in rects:
# print(rects)

