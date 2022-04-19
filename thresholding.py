import cv2
import numpy as np

def readImage(path):
    img1 = cv2.imread(path)
    img2 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    #plt.imshow(img2)
    #plt.show()
    return img2


def threshold_rel(img, lo, hi):
    vmin = np.min(img)
    vmax = np.max(img)
    vlo = vmin + (vmax - vmin) * lo
    vhi = vmin + (vmax - vmin) * hi
    return np.uint8((img >= vlo) & (img <= vhi)) * 255


def threshold_abs(img, lo, hi):
    return np.uint8((img >= lo) & (img <= hi)) * 255
    
    
def get_lanes(img):
    hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    h_channel = hls[:, :, 0]
    l_channel = hls[:, :, 1]
    s_channel = hls[:, :, 2]
    v_channel = hsv[:, :, 2]
    right_lane = threshold_rel(l_channel, 0.8, 1)
    right_lane[:, :750] = 0
    right_lane[:350, :] = 0

    left_lane = threshold_abs(h_channel, 20, 30)
    left_lane &= threshold_rel(v_channel, 0.7, 1.0)
    left_lane[:, 550:] = 0
    left_lane[:350, :] = 0
    img3 = left_lane | right_lane
    return img3
    
