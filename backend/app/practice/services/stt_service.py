import os
import json
import wave
from vosk import Model, KaldiRecognizer
# from pathlib import path

# Path to vosk model (adjust if needed)
VOSK_MODEL_PATH = "softwaremodels/vosk-model-small-en-us-0.15"

if not os.path.exists(VOSK_MODEL_PATH):
    raise RuntimeError("Vosk model not found. Check VOSK_MODEL_PATH")

model = Model(VOSK_MODEL_PATH)


def speech_to_text_from_wav(wav_path: str) -> dict:
    """
    Convert WAV audio to text using Vosk (offline STT)
    """

    if not os.path.exists(wav_path):
        raise FileNotFoundError("WAV file not found")

    with wave.open(wav_path, "rb") as wf:
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
            raise ValueError("Audio must be mono PCM WAV")

        rec = KaldiRecognizer(model, wf.getframerate())
        rec.SetWords(True)

        results = []

        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                results.append(json.loads(rec.Result()))

        results.append(json.loads(rec.FinalResult()))

    # Combine text
    final_text = " ".join([r.get("text", "") for r in results]).strip()

    return {
        "text": final_text,
        "segments": results,
    }
