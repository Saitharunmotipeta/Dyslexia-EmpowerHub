import subprocess
from pathlib import Path

FFMPEG_BIN = "ffmpeg"  # system-installed

def convert_to_wav(input_path: str, output_path: str):
    cmd = [
        FFMPEG_BIN,
        "-y",
        "-i", input_path,
        "-ac", "1",
        "-ar", "16000",
        output_path
    ]
    subprocess.run(cmd, check=True)
