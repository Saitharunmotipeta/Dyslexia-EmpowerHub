import requests
import os

SPEECH_URL = os.getenv("SPEECH_SERVICE_URL")


def recognize_speech(file):
    files = {"file": file}

    response = requests.post(f"{SPEECH_URL}/recognize", files=files)

    if response.status_code != 200:
        raise Exception("Speech service failed")

    return response.json()