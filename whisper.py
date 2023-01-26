import whisper

print("abcd")
model = whisper.load_model("base")

result = model.transcribe("ok.wav")
print(result["text"])


