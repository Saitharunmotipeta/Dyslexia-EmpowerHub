import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ─── BASE DIR (KEEP THIS) ─────────────────────────
BASE_DIR = Path(os.getenv("BASE_DIR", ".")).resolve()

# ─── STATIC ASSETS ───────────────────────────────
STATIC_ASSETS_BASE_URL = os.getenv("STATIC_ASSETS_BASE_URL", "").rstrip("/")

STATIC_TTS_PREFIX = "tts/en"
STATIC_IMAGE_PREFIX = "images/words"

# ─── TEMP DIRS (SINGLE SOURCE) ───────────────────
AUDIO_UPLOAD_DIR = BASE_DIR / os.getenv("UPLOAD_DIR", "temp/audio_uploads")
AUDIO_WAV_DIR = BASE_DIR / os.getenv("WAV_DIR", "temp/audio_wav")

AUDIO_SAMPLES_DIR = BASE_DIR / os.getenv(
    "AUDIO_SAMPLES_DIR", "tests/audio_samples"
)

TTS_AUDIO_DIR = BASE_DIR / os.getenv(
    "TTS_AUDIO_DIR", "app/static/tts_audio"
)

# ─── MODEL PATHS ─────────────────────────────────
FFMPEG_PATH = BASE_DIR / os.getenv("FFMPEG_PATH")
FFPROBE_PATH = BASE_DIR / os.getenv("FFPROBE_PATH")
VOSK_MODEL_PATH = BASE_DIR / os.getenv("VOSK_MODEL_PATH")
PHONEME_MODEL_PATH = BASE_DIR / os.getenv("PHONEME_MODEL_PATH", "")

# ─── ENSURE DIRS ─────────────────────────────────
AUDIO_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
AUDIO_WAV_DIR.mkdir(parents=True, exist_ok=True)
TTS_AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# ─── DEBUG (TEMP) ─────────────────────────────────
print("🔗 BASE_DIR =", BASE_DIR)
print("🔗 VOSK_MODEL_PATH =", VOSK_MODEL_PATH)
print("🔗 EXISTS ?", VOSK_MODEL_PATH.exists())
