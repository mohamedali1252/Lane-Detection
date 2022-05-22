from moviepy.editor import VideoFileClip
from extractCarFromVideo import detect_cars

# input_video = sys.argv[1]
# output_video = sys.argv[2]

input_video = "project_video.mp4"
output_video = "out.mp4"

clip = VideoFileClip(input_video).subclip(0, 5)
clip.set_fps(20)
out_clip = clip.fl_image( detect_cars )
out_clip.write_videofile(output_video, audio=False)
