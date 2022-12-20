import requests
from api_secrets import API_KEY_ASSEMBLYAI
import sys

filename = "output.wav"
upload_endpoint = "https://api.assemblyai.com/v2/upload"
transcript_endpoint = "https://api.assemblyai.com/v2/transcript/sentences"

headers = {'authorization': API_KEY_ASSEMBLYAI}
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

def transcribe(audio_url):
    transcript_request = { "audio_url": audio_url,
    "language_code":"ja" ,
}

    transcript_response = requests.post(transcript_endpoint, json=transcript_request, headers=headers)

    job_id = transcript_response.json()['id']
    return job_id


def poll(transcipt_id):
    polling_endpoint = transcript_endpoint + '/' + transcipt_id
    polling_response = requests.get(polling_endpoint, headers=headers)
    return polling_response.json()

def get_transcription_result_url(audio_url):
    transcipt_id = transcribe(audio_url)
    while True:
        data = poll(transcipt_id)
        if data['status'] == 'completed':
            return data, None
        elif data['status'] == 'error':
            return data, data["error"]

audio_url = uplaod(filename)
data, error = get_transcription_result_url(audio_url)
machine_words = str(data['words'])
text_filename = filename + "-text"
machine_filename = filename + "-machine"

with open(text_filename, 'w',encoding = 'utf-8') as f:
            f.write(data['text'])
with open(machine_filename, 'w',encoding = 'utf-8') as n:
            n.write(machine_words)
print(data)
