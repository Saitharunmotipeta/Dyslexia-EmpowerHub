import re


def detect_type(text: str) -> str:
    """
    Decide if input is a single word or a sentence.
    Dyslexia-safe rule: spaces decide.
    """
    cleaned = text.strip()
    return "sentence" if " " in cleaned else "word"


def normalize_text(text: str) -> str:
    """
    Lowercase and remove unsafe punctuation.
    """
    return re.sub(r"[^a-zA-Z\s]", "", text).lower().strip()
