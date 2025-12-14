import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

AUDIO_RAW_DIR = os.path.join(BASE_DIR, "storage", "audio_raw")
AUDIO_WAV_DIR = os.path.join(BASE_DIR, "storage", "audio_wav")

os.makedirs(AUDIO_RAW_DIR, exist_ok=True)
os.makedirs(AUDIO_WAV_DIR, exist_ok=True)
