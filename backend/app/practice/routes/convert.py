from fastapi import HTTPException, Depends
from app.practice.services.audio_service import convert_to_wav
from app.auth.dependencies import get_current_user_id


def convert_audio(file_id: str, user_id: int = Depends(get_current_user_id),):
    try:
        wav_path = convert_to_wav(file_id, user_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Uploaded audio not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audio conversion failed: {e}")

    return {
        "file_id": file_id,
        "wav_path": wav_path,
        "message": "Audio converted to WAV",
    }
