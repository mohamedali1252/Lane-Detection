from LaneLines import LaneLines
from birdEye import *
from thresholding import *
from moviepy.editor import VideoFileClip
import cv2


lanelines = LaneLines()


def process_image(img):
    M, Minv = perspective_transform()
    warped_img1 = warp_perspective(img, img.shape[1::-1], M)
    img2 = get_lanes(warped_img1)
    img3 = lanelines.forward(img2)
    warped_img2 = warp_perspective(img3, img3.shape[1::-1], Minv)
    out_img = cv2.addWeighted(img, 1, warped_img2, 0.5, 0)
    img4 = lanelines.plot(out_img)
    return img4


input_video = sys.argv[1]
output_video = sys.argv[2]

clip = VideoFileClip(input_video)

out_clip = clip.fl_image( process_image )
out_clip.write_videofile(output_video, audio=False)