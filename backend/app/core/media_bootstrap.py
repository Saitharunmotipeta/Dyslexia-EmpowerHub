# app/core/mediaprocessor.py

import os
from dotenv import load_dotenv
from pydub import AudioSegment

from app.core.paths import BASE_DIR, FFMPEG_PATH, FFPROBE_PATH

load_dotenv()

# ─── VALIDATION ──────────────────────────────────
if not FFMPEG_PATH.exists():
    raise RuntimeError(f"FFmpeg not found at {FFMPEG_PATH}")

if not FFPROBE_PATH.exists():
    raise RuntimeError(f"FFprobe not found at {FFPROBE_PATH}")

# ─── FORCE ENVIRONMENT FOR PYDUB ─────────────────
os.environ["FFMPEG_BINARY"] = str(FFMPEG_PATH)
os.environ["FFPROBE_BINARY"] = str(FFPROBE_PATH)

# Ensure ffmpeg is on PATH (Windows-safe)
os.environ["PATH"] = (
    str(FFMPEG_PATH.parent)
    + os.pathsep
    + os.environ.get("PATH", "")
)

# ─── FORCE PYDUB BINDINGS ─────────────────────────
AudioSegment.converter = str(FFMPEG_PATH)
AudioSegment.ffprobe = str(FFPROBE_PATH)

print("✅ FFmpeg initialized:", FFMPEG_PATH)
print("✅ FFprobe initialized:", FFPROBE_PATH)
