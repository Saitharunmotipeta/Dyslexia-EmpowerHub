import os
import uuid
from pydub import AudioSegment

TEMP_UPLOAD_DIR = "temp/audio_uploads"
TEMP_WAV_DIR = "temp/audio_wav"

os.makedirs(TEMP_WAV_DIR, exist_ok=True)


def convert_to_wav(file_id: str) -> str:
    """
    Convert uploaded audio file to WAV (16kHz, mono).
    Returns path to wav file.
    """

    # Find uploaded file by file_id
    source_file = None
    for f in os.listdir(TEMP_UPLOAD_DIR):
        if f.startswith(file_id):
            source_file = os.path.join(TEMP_UPLOAD_DIR, f)
            break

    if not source_file:
        raise FileNotFoundError("Uploaded audio not found")

    # Load audio
    audio = AudioSegment.from_file(source_file)

    # Normalize for STT
    audio = (
        audio.set_channels(1)        # mono
             .set_frame_rate(16000)   # 16kHz
    )

    wav_filename = f"{file_id}.wav"
    wav_path = os.path.join(TEMP_WAV_DIR, wav_filename)

    audio.export(wav_path, format="wav")

    return wav_path
