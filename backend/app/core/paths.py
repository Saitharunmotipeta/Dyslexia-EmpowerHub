# import os
# from pathlib import Path
# from dotenv import load_dotenv

# load_dotenv()

# # ────────────────────────────────────────────────
# # 🌍 ENVIRONMENT SWITCH (SINGLE SOURCE)
# # ────────────────────────────────────────────────
# ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()
# IS_DEV = ENVIRONMENT == "development"
# IS_PROD = ENVIRONMENT == "production"

# # ────────────────────────────────────────────────
# # 📁 BASE DIR (KEEP THIS – USED EVERYWHERE)
# # ────────────────────────────────────────────────
# BASE_DIR = Path(os.getenv("BASE_DIR", ".")).resolve()

# # ────────────────────────────────────────────────
# # 🌐 STATIC ASSETS (PROD-FIRST)
# # ────────────────────────────────────────────────
# STATIC_ASSETS_BASE_URL = os.getenv("STATIC_ASSETS_BASE_URL", "").rstrip("/")

# # agreed naming (matches your static repo)
# STATIC_TTS_PREFIX = "tts/en"
# STATIC_IMAGE_PREFIX = "images/words"

# # helper builders (safe to import anywhere)
# def static_tts_url(word: str, pace: str) -> str | None:
#     if not STATIC_ASSETS_BASE_URL:
#         return None
#     return f"{STATIC_ASSETS_BASE_URL}/{STATIC_TTS_PREFIX}/{word}_{pace}.wav"


# def static_image_url(word: str) -> str | None:
#     if not STATIC_ASSETS_BASE_URL:
#         return None
#     return f"{STATIC_ASSETS_BASE_URL}/{STATIC_IMAGE_PREFIX}/{word}.png"


# # ────────────────────────────────────────────────
# # ⏱️ TEMP / RUNTIME DIRS (ALWAYS EPHEMERAL)
# # ────────────────────────────────────────────────
# AUDIO_UPLOAD_DIR = BASE_DIR / os.getenv("UPLOAD_DIR", "temp/audio_uploads")
# AUDIO_WAV_DIR = BASE_DIR / os.getenv("WAV_DIR", "temp/audio_wav")

# # Runtime-only caches (TTL controlled)
# TTS_CACHE_DIR = BASE_DIR / "runtime_cache" / "tts"
# STT_CACHE_DIR = BASE_DIR / "runtime_cache" / "stt"

# AUDIO_SAMPLES_DIR = BASE_DIR / os.getenv(
#     "AUDIO_SAMPLES_DIR", "tests/audio_samples"
# )

# for d in [
#     AUDIO_UPLOAD_DIR,
#     AUDIO_WAV_DIR,
#     TTS_CACHE_DIR,
#     STT_CACHE_DIR,
# ]:
#     d.mkdir(parents=True, exist_ok=True)

# # ────────────────────────────────────────────────
# # 🧠 MODELS / BINARIES (ENV-AGNOSTIC)
# # ────────────────────────────────────────────────
# FFMPEG_PATH = BASE_DIR / os.getenv("FFMPEG_PATH")
# FFPROBE_PATH = BASE_DIR / os.getenv("FFPROBE_PATH")
# VOSK_MODEL_PATH = BASE_DIR / os.getenv("VOSK_MODEL_PATH")
# PHONEME_MODEL_PATH = BASE_DIR / os.getenv("PHONEME_MODEL_PATH", "")

# # ────────────────────────────────────────────────
# # 🔍 DEBUG (DEV-ONLY, SAFE)
# # ────────────────────────────────────────────────
# if IS_DEV:
#     print("🔗 ENVIRONMENT =", ENVIRONMENT)
#     print("🔗 BASE_DIR =", BASE_DIR)
#     print("🔗 STATIC_ASSETS_BASE_URL =", STATIC_ASSETS_BASE_URL or "❌ not set")
#     print("🔗 VOSK_MODEL_PATH =", VOSK_MODEL_PATH)
#     print("🔗 VOSK EXISTS ?", VOSK_MODEL_PATH.exists())
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ────────────────────────────────────────────────
# 🌍 ENVIRONMENT SWITCH (SINGLE SOURCE OF TRUTH)
# ────────────────────────────────────────────────
ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()
IS_DEV = ENVIRONMENT == "development"
IS_PROD = ENVIRONMENT == "production"

# ────────────────────────────────────────────────
# 📁 BASE DIR (USED EVERYWHERE)
# ────────────────────────────────────────────────
BASE_DIR = Path(os.getenv("BASE_DIR", ".")).resolve()

# ────────────────────────────────────────────────
# 🌐 STATIC ASSETS (CDN / RENDER)
# ────────────────────────────────────────────────
STATIC_ASSETS_BASE_URL = os.getenv("STATIC_ASSETS_BASE_URL", "").rstrip("/")

STATIC_TTS_PREFIX = "tts/en"
STATIC_IMAGE_PREFIX = "images/words"

def static_tts_url(word: str, pace: str) -> str | None:
    if not STATIC_ASSETS_BASE_URL:
        return None
    return f"{STATIC_ASSETS_BASE_URL}/{STATIC_TTS_PREFIX}/{pace}/{word}.wav"

def static_image_url(word: str) -> str | None:
    if not STATIC_ASSETS_BASE_URL:
        return None
    return f"{STATIC_ASSETS_BASE_URL}/{STATIC_IMAGE_PREFIX}/{word}.jpg"

# ────────────────────────────────────────────────
# ⏱️ RUNTIME / TEMP DIRECTORIES (EPHEMERAL)
# ────────────────────────────────────────────────
AUDIO_UPLOAD_DIR = BASE_DIR / os.getenv("UPLOAD_DIR", "temp/audio_uploads")
AUDIO_WAV_DIR = BASE_DIR / os.getenv("WAV_DIR", "temp/audio_wav")

TTS_CACHE_DIR = BASE_DIR / "runtime_cache" / "tts"
STT_CACHE_DIR = BASE_DIR / "runtime_cache" / "stt"

for d in [
    AUDIO_UPLOAD_DIR,
    AUDIO_WAV_DIR,
    TTS_CACHE_DIR,
    STT_CACHE_DIR,
]:
    d.mkdir(parents=True, exist_ok=True)

# ────────────────────────────────────────────────
# 🔊 TTS CONFIG (ENGINE / API BASED)
# ────────────────────────────────────────────────
TTS_ENGINE = os.getenv("TTS_ENGINE", "browser")  
# examples: browser | web_speech | external_api

TTS_CACHE_ENABLED = os.getenv("TTS_CACHE_ENABLED", "true").lower() == "true"
TTS_CACHE_TTL_MINUTES = int(os.getenv("TTS_CACHE_TTL_MINUTES", "15"))

# Optional (only if external API is used later)
TTS_API_URL = os.getenv("TTS_API_URL", "")
TTS_API_KEY = os.getenv("TTS_API_KEY", "")

# ────────────────────────────────────────────────
# 🗣️ STT CONFIG (BROWSER-FIRST)
# ────────────────────────────────────────────────
STT_ENGINE = os.getenv("STT_ENGINE", "browser")
# browser | web_speech | external_api

STT_API_URL = os.getenv("STT_API_URL", "")
STT_API_KEY = os.getenv("STT_API_KEY", "")

# ────────────────────────────────────────────────
# 🔍 DEV DEBUG (SAFE)
# ────────────────────────────────────────────────
if IS_DEV:
    print("🔧 ENVIRONMENT =", ENVIRONMENT)
    print("📁 BASE_DIR =", BASE_DIR)
    print("🌐 STATIC_ASSETS =", STATIC_ASSETS_BASE_URL or "❌ not set")
    print("🔊 TTS_ENGINE =", TTS_ENGINE)
    print("🗣️ STT_ENGINE =", STT_ENGINE)
