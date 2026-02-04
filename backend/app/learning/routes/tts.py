# app/learning/routes/tts.py

from fastapi import HTTPException
from sqlalchemy.orm import Session
import os

from app.learning.models.word import Word

STATIC_BASE_URL = os.getenv("STATIC_ASSETS_BASE_URL", "").rstrip("/")

PACE_DEFAULTS = {
    "slow": 0.75,
    "medium": 1.0,
    "fast": 1.25,
}


def tts_word_handler(
    db: Session,
    word_id: int,
    pace_mode: str,
    pace_value: int | None = None,
    custom_text: str | None = None,
):
    word = db.query(Word).filter(Word.id == word_id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")

    text = word.text.lower()

    # ─────────────────────────────
    # STATIC TTS (CDN)
    # ─────────────────────────────
    if pace_mode in PACE_DEFAULTS:
        if not STATIC_BASE_URL:
            raise HTTPException(
                status_code=500,
                detail="STATIC_ASSETS_BASE_URL not configured"
            )

        return {
            "mode": "static",
            "word_id": word.id,
            "text": text,
            "pace": pace_mode,
            "pace_value":pace_value,
            "audio_url": f"{STATIC_BASE_URL}/tts/en/{pace_mode}/{text}.wav",
            "image_url": f"{STATIC_BASE_URL}/images/words/{text}.jpg",
        }

    # ─────────────────────────────
    # CUSTOM TTS (BROWSER)
    # ─────────────────────────────
    if pace_mode == "custom":
        speak_text = custom_text or text

        return {
            "mode": "browser",
            "word_id": word.id,
            "text": speak_text,
            "speech_rate": 1.0,   # browser-controlled
            "instruction": "Use Web Speech API",
            "image_url": (
                f"{STATIC_BASE_URL}/images/words/{text}.jpg"
                if STATIC_BASE_URL else None
            ),
        }

    raise HTTPException(
        status_code=400,
        detail="Invalid pace_mode (slow | medium | fast | custom)"
    )
