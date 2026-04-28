import requests
import os
from fastapi import UploadFile

SPEECH_URL = os.getenv("SPEECH_SERVICE_URL")



def recognize_speech(file: UploadFile):
    file.file.seek(0)  # 🔥 CRITICAL
    # print("qwert")

    files = {
        "file": (
            file.filename,
            file.file,
            file.content_type or "audio/wav"
        )
    }
    # print({SPEECH_URL})

    response = requests.post(f"{SPEECH_URL}", files=files)
    # print("12")
    if response.status_code != 200:
        print("Speech error:", response.text)  # 🔥 DEBUG
        raise Exception("Speech service failed")

    return response.json()