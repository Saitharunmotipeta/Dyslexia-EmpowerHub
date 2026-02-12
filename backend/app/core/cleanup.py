import os
import time
from pathlib import Path
from dotenv import load_dotenv

from app.core.paths import AUDIO_UPLOAD_DIR, AUDIO_WAV_DIR

# Load env vars
load_dotenv()  # 👈 moved to main.py for better control over load order

# =========================
# CONFIG
# =========================
DELETE_TEMP_AUDIO = os.getenv("DELETE_TEMP_AUDIO", "true").lower() == "true"

# TTL from env (minutes → seconds)
TTL_MINUTES = int(os.getenv("TEMP_AUDIO_TTL_MINUTES", "60"))
MAX_AGE_SECONDS = TTL_MINUTES * 60

# =========================
# HELPERS
# =========================
def _cleanup_dir(base_dir: Path) -> int:
    """
    Delete files older than MAX_AGE_SECONDS inside base_dir.
    Preserves directory structure.
    Returns number of deleted files.
    """
    if not base_dir.exists():
        return 0

    now = time.time()
    deleted_count = 0

    for root, _, files in os.walk(base_dir):
        for name in files:
            file_path = Path(root) / name
            try:
                age = now - file_path.stat().st_mtime
                if age > MAX_AGE_SECONDS:
                    file_path.unlink()
                    deleted_count += 1
            except Exception:
                # swallow errors – cleanup must never crash app
                pass

    return deleted_count


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

    print(f"🧹 Temp audio cleanup started (TTL={TTL_MINUTES} min)")

    uploads_deleted = _cleanup_dir(AUDIO_UPLOAD_DIR)
    wavs_deleted = _cleanup_dir(AUDIO_WAV_DIR)

    total = uploads_deleted + wavs_deleted

    print(
        f"✅ Temp audio cleanup complete → "
        f"uploads: {uploads_deleted}, "
        f"wav: {wavs_deleted}, "
        f"total: {total}"
    )
