import os
import uuid
import pyttsx3

AUDIO_DIR = "app/static/tts_audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

# Speech rate mapping (Windows-friendly)
RATE_MAP = {
    "slow": 50,
    "medium": 100,
    "fast": 140,
}

MAX_TEXT_LENGTH = 500


def generate_tts_audio(text: str, speed: str = "medium") -> str:
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")

    if len(text) > MAX_TEXT_LENGTH:
        raise ValueError("Text too long for TTS")

    rate = RATE_MAP.get(speed, RATE_MAP["medium"])

    filename = f"{uuid.uuid4().hex}.wav"
    filepath = os.path.join(AUDIO_DIR, filename)

    engine = pyttsx3.init()
    engine.setProperty("rate", rate)

    # Prefer English voice if available
    voices = engine.getProperty("voices")
    for voice in voices:
        if "english" in voice.name.lower():
            engine.setProperty("voice", voice.id)
            break

    engine.save_to_file(text, filepath)
    engine.runAndWait()
    engine.stop()

    return f"/static/tts_audio/{filename}"
