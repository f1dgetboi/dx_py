
import cv2
import pysrt
from PIL import ImageFont, ImageDraw, Image
import moviepy.editor as mp
import numpy as np
from moviepy.editor import *

# Open the input video file
input_video = cv2.VideoCapture(r'testing-videos\testingvideo.mp4')

# Get the video dimensions and FPS
width = int(input_video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(input_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(input_video.get(cv2.CAP_PROP_FPS))
print(fps)
# Set up the output video file
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_video = cv2.VideoWriter('new_video.avi', fourcc, fps, (width, height))


audio_clip = AudioFileClip('audio\output.mp3')

# Load the SRT file
subs = pysrt.open('new.srt')


# Define the font properties for the text overlay
font_scale = 1
color = (255, 255, 255) # white color
thickness = 2

# Loop through each frame of the video and overlay text within the time range
while True:
    ret, frame = input_video.read()
    if not ret:
        break

    # Get the current time (in seconds)
    current_frame = int(input_video.get(cv2.CAP_PROP_POS_FRAMES))
    # Loop through each subtitle in the SRT file
    for sub in subs:

        start_time = sub.start.minutes * 60 + sub.start.seconds
        end_time = sub.start.minutes * 60 + sub.end.seconds

        if start_time <= int(current_frame) / fps  <= end_time:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(frame_rgb)
            draw = ImageDraw.Draw(pil_image)
            #print(f"{sub.text}")
            font = ImageFont.truetype('C:\Windows\Fonts\BIZ-UDMinchoM.TTC', 50)
            draw.text((50, 300), f"{sub.text}", font=font)
            rgb_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            #cv2.putText(frame, sub.text, (50, 50), font, font_scale, color, thickness, cv2.LINE_AA)
            #print(f"start: {start_time}, end: {end_time} current time: {current_frame/fps} text: {sub.text}")

    output_video.write(rgb_image)

# Release the video objects
input_video.release()
output_video.release()
videoclip = VideoFileClip("new_video.avi")
new_audioclip = CompositeAudioClip([audio_clip])
videoclip.audio = new_audioclip
videoclip.write_videofile("new_filename.mp4")
print("susceeded")