import os
from pathlib import Path

# ────────────────────────────────────────────────
# 🌍 ENVIRONMENT
# ────────────────────────────────────────────────
ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()
IS_DEV = ENVIRONMENT == "development"
IS_PROD = ENVIRONMENT == "production"

# ────────────────────────────────────────────────
# 📁 BASE DIRECTORY
# ────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ────────────────────────────────────────────────
# 🌐 STATIC ASSETS (CDN / Render Static Repo)
# ────────────────────────────────────────────────
STATIC_ASSETS_BASE_URL = os.getenv("STATIC_ASSETS_BASE_URL", "").rstrip("/")

STATIC_TTS_PREFIX = "tts/en"
STATIC_IMAGE_PREFIX = "images/words"


def static_tts_url(word: str, pace: str) -> str | None:
    """
    Build static TTS audio URL.
    Example:
    https://cdn-url/tts/en/slow/celebration.wav
    """
    if not STATIC_ASSETS_BASE_URL:
        return None
    return f"{STATIC_ASSETS_BASE_URL}/{STATIC_TTS_PREFIX}/{pace}/{word}.wav"


def static_image_url(word: str) -> str | None:
    """
    Build static image URL.
    Example:
    https://cdn-url/images/words/celebration.jpg
    """
    if not STATIC_ASSETS_BASE_URL:
        return None
    return f"{STATIC_ASSETS_BASE_URL}/{STATIC_IMAGE_PREFIX}/{word}.jpg"


# ────────────────────────────────────────────────
# 🔊 ENGINE CONFIG (Toggle-ready)
# ────────────────────────────────────────────────
STT_ENGINE = os.getenv("STT_ENGINE", "browser")
TTS_ENGINE = os.getenv("TTS_ENGINE", "static")