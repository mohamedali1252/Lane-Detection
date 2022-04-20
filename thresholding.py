import cv2
import numpy as np
import matplotlib.pyplot as plt

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


def hls_channels(img):
    hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
    return hls[:,:,0], hls[:,:,1], hls[:,:,2]

def hsv_channels(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2HSV)[:,:,2]

# img = readImage("../test_images/challenge_video_frame_10.jpg")
# h, l, s = hls_channels(img)
# v = hsv_channels(img)
# img = threshold_rel(l, 0.8, 1)

# cv2.namedWindow("image", cv2.WINDOW_NORMAL)
# cv2.createTrackbar("low_threshold", "image", 0, 100, lambda x: print(x))
# cv2.createTrackbar("high_threshold", "image", 0, 100, lambda x: print(x))
# # cv2.createTrackbar("low_abs_threshold", "image", 0, 255, lambda x: print(x))
# # cv2.createTrackbar("high_abs_threshold", "image", 0, 255, lambda x: print(x))

# while True:
#     cv2.imshow("image", img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

#     low = cv2.getTrackbarPos("low_threshold", "image")
#     high = cv2.getTrackbarPos("high_threshold", "image")
#     img = threshold_rel(v, low/100, high/100)

#     # low = cv2.getTrackbarPos("low_abs_threshold", "image")
#     # high = cv2.getTrackbarPos("high_abs_threshold", "image")
#     # img = threshold_abs(v, low, high)

#     cv2.imshow("image", img)


def get_lanes(img):
    h, l, s = hls_channels(img)
    v = hsv_channels(img)
    right_lane = threshold_rel(l, 0.8, 1)
    right_lane[:, :750] = 0
    right_lane[:350, :] = 0

    left_lane = threshold_abs(h, 20, 30)
    left_lane &= threshold_rel(v, 0.7, 1.0)
    left_lane[:, 550:] = 0
    left_lane[:350, :] = 0
    img3 = left_lane | right_lane
    return img3, right_lane, left_lane

