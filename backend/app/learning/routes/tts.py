from fastapi import HTTPException
from sqlalchemy.orm import Session
import os

from app.learning.models.word import Word
from app.learning.services.tts_services import generate_runtime_tts

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────

STATIC_BASE_URL = os.getenv("STATIC_ASSETS_BASE_URL", "").rstrip("/")

PACE_DEFAULTS = {
    "slow": 50,
    "medium": 80,
    "fast": 110,
}

# ─────────────────────────────────────────────
# HANDLER
# ─────────────────────────────────────────────

def tts_word_handler(
    db: Session,
    word_id: int,
    pace_mode: str,
    pace_value: int | None = None,
):
    # ── Fetch word ────────────────────────────
    word = db.query(Word).filter(Word.id == word_id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")

    text = word.text.lower()

    # ─────────────────────────────────────────
    # STATIC MODES (slow / medium / fast)
    # ─────────────────────────────────────────
    if pace_mode in PACE_DEFAULTS:
        pace = PACE_DEFAULTS[pace_mode]

        # ✅ Production → static assets
        if STATIC_BASE_URL:
            return {
                "word_id": word.id,
                "pace_mode": pace_mode,
                "pace_value": pace,
                "source": "static",
                "audio_url": f"{STATIC_BASE_URL}/tts/en/{pace_mode}/{text}.wav",
                "image_url": f"{STATIC_BASE_URL}/images/words/{text}.jpg",
            }

        # 🔁 Development fallback → runtime TTS
        audio_url = generate_runtime_tts(
            text=text,
            pace=pace
        )

        return {
            "word_id": word.id,
            "pace_mode": pace_mode,
            "pace_value": pace,
            "source": "runtime-fallback",
            "audio_url": audio_url,
            "image_url": None,
        }

    # ─────────────────────────────────────────
    # CUSTOM MODE (runtime only, cached + TTL)
    # ─────────────────────────────────────────
    if pace_mode == "custom":
        if pace_value is None:
            raise HTTPException(
                status_code=400,
                detail="pace_value is required when pace_mode=custom"
            )

        audio_url = generate_runtime_tts(
            text=text,
            pace=pace_value
        )

        return {
            "word_id": word.id,
            "pace_mode": "custom",
            "pace_value": pace_value,
            "source": "runtime",
            "audio_url": audio_url,
            "image_url": (
                f"{STATIC_BASE_URL}/images/words/{text}.jpg"
                if STATIC_BASE_URL else None
            ),
        }

    # ─────────────────────────────────────────
    # INVALID MODE
    # ─────────────────────────────────────────
    raise HTTPException(
        status_code=400,
        detail="Invalid pace_mode. Use slow | medium | fast | custom"
    )
