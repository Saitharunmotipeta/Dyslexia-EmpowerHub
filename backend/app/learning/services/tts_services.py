import uuid
import pyttsx3
from pathlib import Path

from app.core.paths import TTS_AUDIO_DIR
# from app.core.config import settings  # if you have one
import os

# Speech rate mapping
RATE_MAP = {
    "slow": 60,
    "medium": 90,
    "fast": 120,
}

MAX_TEXT_LENGTH = 500


def generate_tts_audio(text: str, speed: str = "medium") -> str:
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")

    if len(text) > MAX_TEXT_LENGTH:
        raise ValueError("Text too long for TTS")

    rate = RATE_MAP.get(speed, RATE_MAP["medium"])

    filename = f"{uuid.uuid4().hex}.wav"
    filepath: Path = TTS_AUDIO_DIR / filename

    engine = pyttsx3.init()
    engine.setProperty("rate", rate)

    # Prefer English voice
    for voice in engine.getProperty("voices"):
        if "english" in voice.name.lower():
            engine.setProperty("voice", voice.id)
            break

    engine.save_to_file(text, str(filepath))
    engine.runAndWait()
    engine.stop()

    # 🔗 RETURN PUBLIC URL (not local path)
    base_url = os.getenv("STATIC_ASSETS_BASE_URL", "")
    if base_url:
        return f"{base_url}/tts_audio/{filename}"

    # fallback (local dev)
    return f"/static/tts_audio/{filename}"
