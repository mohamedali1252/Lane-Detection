from thresholding import cv2, np, get_lanes
from birdEye import perspective_transform, warp_perspective
from LaneLines import LaneLines
from phase2 import os, detect_cars

lanelines = LaneLines()

def resizing(img, ratio = 0.33):
    return cv2.resize(img, (int(img.shape[1] * ratio), int(img.shape[0] * ratio)))

def channels_3(img):
    if len(img.shape) < 3:
        return np.dstack((img, img, img))
    return img

def margin(img, thickness = 2):
    img[:thickness, :] = 255
    img[img.shape[0]-thickness:, :] = 255
    img[:, :thickness] = 255
    img[:, img.shape[1]-thickness:] = 255
    return img

def debug(img, img1, img2, img3, img4, img5, img6, img7):
    # vertically aligned 4 images
    out_img = np.concatenate((resizing(channels_3(margin(img1))), resizing(channels_3(margin(img2)))), axis = 0)
    out_img = np.concatenate((out_img, resizing(channels_3(margin(img3)))), axis = 0)
    img4 = cv2.resize(img4, (int(img4.shape[1] * 0.33), int(img4.shape[0] * 0.342)))
    out_img = np.concatenate((out_img, channels_3(margin(img4))), axis = 0)
    
    # horizontally aligned 3 images with large image vertically aligned
    out_img1 = np.concatenate((resizing(channels_3(margin(img7))), resizing(channels_3(margin(img6)))), axis = 1)
    img5 = cv2.resize(img5, (int(img5.shape[1] * 0.341), int(img5.shape[0] * 0.33)))
    out_img1 = np.concatenate((out_img1, channels_3(margin(img5))), axis = 1)
    out_img1 = np.concatenate((channels_3(img), out_img1), axis = 0)

    # the 2 combinations horizontally aligned
    out_img = np.concatenate((out_img1, out_img), axis = 1)
    return out_img

class ProcessImage:
    def __init__(self, debugMode = False, phase = 2):
        self.debugMode = debugMode
        self.phase = phase
        if self.phase == 1 or self.phase == 2:
            weights_path = os.path.join("yolo-coco","yolov3.weights")
            config_path = os.path.join("yolo-coco","yolov3.cfg")

            self.net = cv2.dnn.readNetFromDarknet(config_path,weights_path)
            self.names = self.net.getLayerNames()
    
    def process_image(self, img):
        if self.phase == 0 or self.phase == 2:
            img2, right, left = get_lanes(img)
            M, Minv = perspective_transform()
            warped_img1 = warp_perspective(img2, img2.shape[1::-1], M)
            img4, img3 = lanelines.forward(warped_img1)
            warped_img2 = warp_perspective(img4, img4.shape[1::-1], Minv)
            out_img = cv2.addWeighted(img, 1, warped_img2, 0.5, 0)
            img5 = lanelines.plot(out_img)
        if self.phase == 1 or self.phase == 2:
            cars_img = detect_cars(img, self.net, self.names)
            img5 = cv2.addWeighted(img, 1, cars_img, 0.5, 0)
        if self.phase == 2:
            cars_img = detect_cars(img, self.net, self.names)
            img5 = cv2.addWeighted(img5, 1, cars_img, 0.5, 0)
        if self.debugMode:
            return debug(img5, right, left, img2, warped_img1, img3, img4, warped_img2)
        return img5
