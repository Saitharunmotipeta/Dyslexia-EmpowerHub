from fastapi import HTTPException
from app.practice.services.audio_service import convert_to_wav
from app.core.paths import AUDIO_WAV_DIR
import os


def convert_audio(file_id: str):
    try:
        wav_path = os.path.join(AUDIO_WAV_DIR, f"{file_id}.wav")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Uploaded audio not found")
    except Exception:
        raise HTTPException(status_code=500, detail="Audio conversion failed")

    return {
        "file_id": file_id,
        "wav_path": wav_path,
        "message": "Audio converted to WAV",
    }
