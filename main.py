import sys
from moviepy.editor import VideoFileClip
from ProcessImage import ProcessImage


input_video = sys.argv[1]
output_video = sys.argv[2]
debugMode = int(sys.argv[3])
print(debugMode)
print(input_video, output_video, debugMode)


# input_video = "challenge_video.mp4"
# output_video = "out.mp4"
# debugMode = True

process = ProcessImage(debugMode = debugMode)


#input_video = '../challenge_video.mp4'
#output_video = 'output_video.mp4'

clip = VideoFileClip(input_video)

out_clip = clip.fl_image( process.process_image )
out_clip.write_videofile(output_video, audio=False)

