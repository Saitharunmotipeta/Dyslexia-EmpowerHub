from fastapi import APIRouter, HTTPException
from pathlib import Path

from app.practice.services.stt_service import speech_to_text_from_wav
from app.core.paths import AUDIO_WAV_DIR

router = APIRouter()


@router.post("/stt/{file_id}")
def speech_to_text(file_id: str):
    wav_path = Path(AUDIO_WAV_DIR) / f"{file_id}.wav"

    if not wav_path.exists():
        raise HTTPException(status_code=404, detail="WAV file not found")

    try:
        result = speech_to_text_from_wav(wav_path)
    except Exception:
        raise HTTPException(status_code=500, detail="Speech-to-text failed")

    return {
        "file_id": file_id,
        "recognized_text": result.get("text", ""),
        "confidence": result.get("confidence"),
    }
