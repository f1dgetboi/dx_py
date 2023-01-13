import requests
from api_secrets import API_KEY_ASSEMBLYAI
import sys
import json
import numpy 
import moviepy as mp

filename = "output.wav"
projectname = "jj"
language = "ja"
upload_endpoint = "https://api.assemblyai.com/v2/upload"
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"

texts = []
starts = []
ends = []
headers = {'authorization': API_KEY_ASSEMBLYAI,"content-type": "application/json"}
def uplaod(filename):
    def read_file(filename, chunk_size=5242880):
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data

    uplaod_response = requests.post(upload_endpoint ,
                            headers=headers,
                            data=read_file(filename))

    audio_url = uplaod_response.json()["upload_url"]
    return audio_url

def transcribe(audio_url,lan):
    transcript_request = { 
    "audio_url": audio_url,
    "language_code": lan
    }

    transcript_response = requests.post(transcript_endpoint, json=transcript_request, headers=headers)

    job_id = transcript_response.json()['id']
    return job_id


def poll(transcipt_id):
    polling_endpoint = transcript_endpoint + '/' + transcipt_id
    polling_response = requests.get(polling_endpoint, headers=headers)
    return polling_response.json()

def get_transcription_result_url(audio_url):
    transcipt_id = transcribe(audio_url,language)
    while True:
        data = poll(transcipt_id)
        if data['status'] == 'completed':
            return data, None
        elif data['status'] == 'error':
            return data, data["error"]

audio_url = uplaod(filename)
data, error = get_transcription_result_url(audio_url)
text_filename = projectname + "-text"


print(data['words'])

for i in data['words']:
    texts.append(i['text'])
    starts.append(i['start'])
    ends.append(i['end'])

print(texts,starts,ends)

with open(text_filename, 'w',encoding = 'utf-8') as f:
            f.write(str(texts) + "\n" + str(starts) + "\n" + str(ends))


def write_on_video(lan):
    if lan == "ja":
        pass
    else:
        pass 