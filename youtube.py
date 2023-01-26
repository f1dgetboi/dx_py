from pytube import YouTube
import os 
import moviepy.editor as mp
def download_video(url):
    yt = YouTube(url)
    video = yt.streams.filter().first()
    video.download()

    print('Video downloaded successfully!')
    return video
download_video('https://www.youtube.com/watch?v=H0hnsdRfimg')
# my_clip = mp.VideoFileClip("ok.mp4")
# filename = "output.wav"
# my_clip.audio.write_audiofile(filename)
