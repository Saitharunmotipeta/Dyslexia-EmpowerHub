from fastapi import HTTPException
from app.practice.services.audio_service import convert_to_wav


def convert_audio(file_id: str):
    try:
        wav_path = convert_to_wav(file_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Uploaded audio not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audio conversion failed: {e}")

    return {
        "file_id": file_id,
        "wav_path": wav_path,
        "message": "Audio converted to WAV",
    }
