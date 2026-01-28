import os
import time
from pathlib import Path
from dotenv import load_dotenv

from app.core.paths import AUDIO_UPLOAD_DIR, AUDIO_WAV_DIR

# Load env vars
load_dotenv()

# =========================
# CONFIG
# =========================
DELETE_TEMP_AUDIO = os.getenv("DELETE_TEMP_AUDIO", "true").lower() == "true"

# seconds (1 hour)
MAX_AGE_SECONDS = 60 * 60

# =========================
# HELPERS
# =========================
def _cleanup_dir(base_dir: Path):
    """
    Delete files older than MAX_AGE_SECONDS inside base_dir.
    Preserves directory structure.
    """
    if not base_dir.exists():
        return

    now = time.time()

    for root, _, files in os.walk(base_dir):
        for name in files:
            file_path = Path(root) / name
            try:
                age = now - file_path.stat().st_mtime
                if age > MAX_AGE_SECONDS:
                    file_path.unlink()
                    print(f"🧹 Deleted temp file: {file_path}")
            except Exception as e:
                print(f"⚠️ Failed to delete {file_path}: {e}")


# =========================
# ENTRY POINT
# =========================
def cleanup_temp_audio():
    """
    Cleans up temp audio files if enabled.
    Safe to call repeatedly.
    """
    if not DELETE_TEMP_AUDIO:
        print("🛑 Temp audio cleanup disabled (DELETE_TEMP_AUDIO=false)")
        return

    print("🧹 Running temp audio cleanup...")
    _cleanup_dir(AUDIO_UPLOAD_DIR)
    _cleanup_dir(AUDIO_WAV_DIR)
    print("✅ Temp audio cleanup complete")
