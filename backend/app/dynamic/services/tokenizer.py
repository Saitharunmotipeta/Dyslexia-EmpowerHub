from typing import List


def tokenize_sentence(text: str) -> List[str]:
    """
    Break sentence into words.
    Dyslexia-first: keep sentence structure.
    """
    return [w for w in text.split() if len(w) > 1]
