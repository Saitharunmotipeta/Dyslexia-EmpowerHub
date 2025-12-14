# media/audio_processor.py
from media.ffmpeg_utils import convert_to_wav

def prepare_audio_for_stt(raw_file: str) -> str:
    wav_path = raw_file.replace(".mp3", ".wav")
    convert_to_wav(raw_file, wav_path)
    return wav_path
