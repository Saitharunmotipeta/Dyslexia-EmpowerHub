import subprocess
import shutil
import os

def extract_phonemes(text: str):
    """
    Extract phonemes using eSpeak.
    Returns list[str] or None
    """

    if not text:
        return None

    espeak_path = shutil.which("espeak")

    if not espeak_path:
        raise RuntimeError("espeak not installed or not in PATH")

    try:
        result = subprocess.run(
            [espeak_path, "-q", "--ipa", text],
            capture_output=True,
            text=True,
            check=True
        )

        phonemes = result.stdout.strip()

        if not phonemes:
            return None

        return phonemes.split()

    except Exception as e:
        return None
