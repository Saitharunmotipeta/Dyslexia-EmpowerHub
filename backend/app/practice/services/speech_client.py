import requests
import os
from fastapi import UploadFile

SPEECH_URL = os.getenv("NEXT_PUBLIC_SPEECH_SERVICE_URL")


def recognize_speech(file: UploadFile):
    file.file.seek(0)  # 🔥 CRITICAL

    files = {
        "file": (
            file.filename,
            file.file,
            file.content_type or "audio/wav"
        )
    }

    response = requests.post(f"{SPEECH_URL}/recognize", files=files)

    if response.status_code != 200:
        print("Speech error:", response.text)  # 🔥 DEBUG
        raise Exception("Speech service failed")

    return response.json()