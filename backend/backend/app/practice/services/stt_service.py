import json
import wave
from pathlib import Path
from vosk import Model, KaldiRecognizer
from pydub import AudioSegment

# =========================
# PATHS
# =========================
BASE_DIR = Path(__file__).resolve().parents[3]
VOSK_MODEL_PATH = BASE_DIR / "softwaremodels" / "vosk-model-small-en-us-0.15"

if not VOSK_MODEL_PATH.exists():
    raise RuntimeError(f"Vosk model not found at: {VOSK_MODEL_PATH}")

# =========================
# LAZY LOAD MODEL (once)
# =========================
_model = None


def get_model():
    global _model
    if _model is None:
        _model = Model(str(VOSK_MODEL_PATH))
    return _model


# =========================
# HELPERS
# =========================
def _normalize_wav(input_wav: Path) -> Path:
    """
    Ensure WAV is mono, 16-bit PCM, 16000Hz.
    Writes a temp-normalized file beside it.
    """
    normalized = input_wav.with_name(input_wav.stem + "_norm.wav")

    audio = AudioSegment.from_wav(str(input_wav))
    audio = audio.set_channels(1)
    audio = audio.set_frame_rate(16000)
    audio = audio.set_sample_width(2)  # 16-bit PCM

    audio.export(str(normalized), format="wav")
    return normalized


def _log_audio_info(wf):
    print("🎧 WAV INFO -> "
          f"channels={wf.getnchannels()}, "
          f"sampwidth={wf.getsampwidth()}, "
          f"framerate={wf.getframerate()}, "
          f"type={wf.getcomptype()}"
          )


# =========================
# MAIN API
# =========================
def speech_to_text_from_wav(wav_path) -> dict:
    """
    Convert WAV audio to text using Vosk (offline STT).
    Requires mono, 16-bit PCM WAV — auto-fixes if not.
    """

    wav_path = Path(wav_path)

    if not wav_path.exists():
        raise FileNotFoundError(f"WAV file not found: {wav_path}")

    # --- Inspect original file ---
    with wave.open(str(wav_path), "rb") as wf:
        _log_audio_info(wf)

        needs_fix = not (
            wf.getnchannels() == 1
            and wf.getsampwidth() == 2
            and wf.getcomptype() == "NONE"
        )

    # --- Auto-normalize if needed ---
    if needs_fix:
        print("⚠️ WAV not mono/16-bit PCM — normalizing…")
        wav_path = _normalize_wav(wav_path)

    # --- Load final file ---
    with wave.open(str(wav_path), "rb") as wf:
        rec = KaldiRecognizer(get_model(), wf.getframerate())
        rec.SetWords(True)

        results = []
        while True:
            data = wf.readframes(4000)
            if not data:
                break
            if rec.AcceptWaveform(data):
                results.append(json.loads(rec.Result()))

        results.append(json.loads(rec.FinalResult()))

    # --- Build final text ---
    text = " ".join(r.get("text", "") for r in results).strip()
    print("CHANNELS", wf.getnchannels())
    print("WIDTH", wf.getsampwidth())
    print("TYPE", wf.getcomptype())
    print("FRAMERATE", wf.getframerate())


    return {
        "text": text,
        "segments": results,
    }

def speech_to_text(wav_path):
    return speech_to_text_from_wav(wav_path)
