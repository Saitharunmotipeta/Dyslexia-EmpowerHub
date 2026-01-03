from pathlib import Path
import os
from pydub import AudioSegment

# backend/
BASE_DIR = Path(__file__).resolve().parents[3]

UPLOAD_DIR = BASE_DIR / "temp" / "audio_uploads"
WAV_DIR = BASE_DIR / "temp" / "audio_wav"

os.makedirs(WAV_DIR, exist_ok=True)


def convert_to_wav(file_id: str) -> str:
    """
    Find uploaded file by file_id.* and convert to mono 16k WAV.
    Returns absolute wav file path.
    """

    candidates = list(UPLOAD_DIR.glob(f"{file_id}.*"))
    if not candidates:
        raise FileNotFoundError("Uploaded file not found")

    source_file = candidates[0]

    audio = AudioSegment.from_file(source_file)
    audio = audio.set_channels(1).set_frame_rate(16000)

    wav_path = WAV_DIR / f"{file_id}.wav"
    audio.export(wav_path, format="wav")

    return str(wav_path)
