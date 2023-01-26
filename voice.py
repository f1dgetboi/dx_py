import speech_recognition as sr
import moviepy.editor as mp

my_clip = mp.VideoFileClip("test.mp4")
filename = "audio/output.wav"
my_clip.audio.write_audiofile(filename)

def main():

    r = sr.Recognizer()

    with sr.AudioFile(filename) as source:
        r.adjust_for_ambient_noise(source)

        print("Please say something")

        audio = r.listen(source)

        print("Recognizing Now .... ")


        # recognize speech using google
        rec_text =  r.recognize_google(audio, language="ja-JP")
        rec_text = str(rec_text)
        with open('text/readme.txt', 'w',encoding = 'utf-8') as f:
            f.write(rec_text)

        with open("recorded.wav", "wb") as f:
            #f.write(audio.get_wav_data())
            pass
if __name__ == "__main__":
    main()
