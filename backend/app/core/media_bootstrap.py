# app/core/media_bootstrap.py

"""
Media bootstrap (BROWSER-FIRST)

✔ STT handled in browser (Web Speech API)
✔ TTS handled via browser OR runtime TTS
✔ No ffmpeg dependency
✔ Safe for free-tier deployment
"""

import os
from dotenv import load_dotenv

load_dotenv()

print("🔊 TTS_ENGINE = browser")
print("🗣️ STT_ENGINE = browser")
# print("⚠️ FFmpeg is NOT required (by design)")
