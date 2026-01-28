from pathlib import Path
import os
from pydub import AudioSegment
from app.core.paths import AUDIO_UPLOAD_DIR as UPLOAD_DIR
from app.core.paths import AUDIO_WAV_DIR as WAV_DIR

def convert_to_wav(file_id: str, user_id: int) -> str:
    """
    Find uploaded file by file_id.* and convert to mono 16k WAV.
    Returns absolute wav file path.
    """

    user_dir = UPLOAD_DIR / str(user_id)
    candidates = list(user_dir.glob(f"{file_id}.*"))
    if not candidates:
        raise FileNotFoundError("Uploaded file not found")

    source_file = candidates[0]

    audio = AudioSegment.from_file(source_file)
    audio = audio.set_channels(1).set_frame_rate(16000)

    wav_path = WAV_DIR / f"{file_id}.wav"
    audio.export(wav_path, format="wav")

    return str(wav_path)
