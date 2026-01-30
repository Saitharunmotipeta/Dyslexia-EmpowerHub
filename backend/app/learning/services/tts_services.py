import time
from pathlib import Path
import pyttsx3

from app.core.paths import TTS_CACHE_DIR

TTL_SECONDS = 15 * 60  # 15 minutes


def generate_runtime_tts(text: str, pace: int) -> str:
    pace = max(40, min(pace, 200))

    # deterministic cache key
    safe_text = text.lower().replace(" ", "_")
    filename = f"{safe_text}_custom_{pace}.wav"
    filepath: Path = TTS_CACHE_DIR / filename

    # CACHE HIT
    if filepath.exists():
        age = time.time() - filepath.stat().st_mtime
        if age < TTL_SECONDS:
            print("♻️ TTS cache hit")
            return f"/runtime-tts/{filename}"

    # CACHE MISS
    print("🆕 Generating runtime TTS")

    engine = pyttsx3.init()
    engine.setProperty("rate", pace)

    for voice in engine.getProperty("voices"):
        if "english" in voice.name.lower():
            engine.setProperty("voice", voice.id)
            break

    engine.save_to_file(text, str(filepath))
    engine.runAndWait()
    engine.stop()

    return f"/runtime-tts/{filename}"
