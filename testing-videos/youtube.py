from pytube import YouTube
import os 
import moviepy.editor as mp
def download_video(url):
    yt = YouTube(url)
    video = yt.streams.filter().first()
    video.download()

    print('Video downloaded successfully!')
    return video

my_clip = mp.VideoFileClip(download_video('https://www.youtube.com/watch?v=2Ax_EIb1zks&t=0s'))
filename = "bruh.wav"
my_clip.audio.write_audiofile(filename)
