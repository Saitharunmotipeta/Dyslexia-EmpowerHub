from fastapi import HTTPException, Depends
from pathlib import Path
from app.practice.services.stt_service import speech_to_text_from_wav
from app.auth.dependencies import get_current_user_id
from app.core.paths import AUDIO_WAV_DIR

def speech_to_text(file_id: str, user_id: int = Depends(get_current_user_id),):
    wav_path = Path(AUDIO_WAV_DIR) / str(user_id) / f"{file_id}.wav"
    print("🔍 DEBUG wav_path =", wav_path, "exists?", wav_path.exists())

    if not wav_path.exists():
        raise HTTPException(status_code=404, detail="WAV file not found")

    if wav_path.stat().st_size == 0:
        raise HTTPException(status_code=400, detail="WAV file is empty")

    try:
        result = speech_to_text_from_wav(str(wav_path))
        print(f"🎧 STT on {wav_path}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Speech-to-text failed: {e}")

    return {
        "file_id": file_id,
        "recognized_text": result.get("text", ""),
    }
