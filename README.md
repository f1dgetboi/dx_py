## ファイルについて
voice.py声をテキストファイルに入れる（OUT.txt）
video.pyでそれを動画に乗せる（まだ終わっていない）
@ -12,24 +11,28 @@
pip install python-opencv
```
moviepy
```
pip install moviepy
```
## voice.pyに関して
マイクではなくて音声ファイルで声の認証をしたいときは
```
with sr.Microphone() as source:
```
ではなくて、
```
with sr.AudioFile(ファイル名) as source:
```
声の認証ができる

動画から音声を抽出するためにはmoviepyをつかう
```
my_clip = mp.VideoFileClip(r"ファイル名")

my_clip.audio.write_audiofile(r"my_result.mp3")
```
my_resultを抽出してできたmp3のファイル名になる。
my_resultを抽出してできたmp3のファイル名になる。だから
```
with sr.AudioFile(my_result.mp3) as source:
```
にしたら動画から抽出できる。
