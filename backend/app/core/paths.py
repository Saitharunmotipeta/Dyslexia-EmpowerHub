from pathlib import Path

# backend/
BASE_DIR = Path(__file__).resolve().parents[3]

# temp directories
AUDIO_UPLOAD_DIR = BASE_DIR /"backend"/ "temp" / "audio_uploads"
AUDIO_WAV_DIR = BASE_DIR /"backend"/ "temp" / "audio_wav"

AUDIO_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
AUDIO_WAV_DIR.mkdir(parents=True, exist_ok=True)
