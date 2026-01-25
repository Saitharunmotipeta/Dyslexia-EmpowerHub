import os
import pathlib
from dotenv import load_dotenv
from pydub import AudioSegment

load_dotenv()

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[2]

ffmpeg_rel = os.getenv("FFMPEG_PATH")
ffprobe_rel = os.getenv("FFPROBE_PATH")

if not ffmpeg_rel or not ffprobe_rel:
    raise RuntimeError("FFMPEG_PATH or FFPROBE_PATH missing in .env")

FFMPEG_PATH = (PROJECT_ROOT / ffmpeg_rel).resolve()
FFPROBE_PATH = (PROJECT_ROOT / ffprobe_rel).resolve()

if not FFMPEG_PATH.exists():
    raise RuntimeError(f"FFmpeg not found at {FFMPEG_PATH}")

if not FFPROBE_PATH.exists():
    raise RuntimeError(f"FFprobe not found at {FFPROBE_PATH}")

# Force environment
os.environ["FFMPEG_BINARY"] = str(FFMPEG_PATH)
os.environ["FFPROBE_BINARY"] = str(FFPROBE_PATH)
os.environ["PATH"] = str(FFMPEG_PATH.parent) + os.pathsep + os.environ.get("PATH", "")

# Force pydub bindings
AudioSegment.converter = str(FFMPEG_PATH)
AudioSegment.ffprobe = str(FFPROBE_PATH)

# print("✅ FFmpeg OK:", FFMPEG_PATH)
# print("✅ FFprobe OK:", FFPROBE_PATH)
