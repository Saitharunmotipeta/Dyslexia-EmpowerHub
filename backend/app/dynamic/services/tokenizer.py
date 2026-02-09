from typing import List


STOP_WORDS = {
    "the", "is", "a", "an", "and", "to", "of", "in", "on"
}


def tokenize_sentence(text: str) -> List[str]:
    """
    Break sentence into meaningful words.
    Dyslexia-first: remove filler words.
    """
    words = text.split()
    return [
        w for w in words
        if len(w) > 2 and w not in STOP_WORDS
    ]
