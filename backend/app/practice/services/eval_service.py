from difflib import SequenceMatcher


def evaluate_similarity(expected_text: str, spoken_text: str) -> dict:
    """
    Compare expected text vs spoken text and return similarity score
    """

    if not expected_text or not spoken_text:
        return {
            "similarity": 0.0,
            "verdict": "invalid_input",
        }

    ratio = SequenceMatcher(
        None,
        expected_text.lower().strip(),
        spoken_text.lower().strip()
    ).ratio()

    similarity_percent = round(ratio * 100, 2)

    verdict = (
        "excellent" if similarity_percent >= 85 else
        "good" if similarity_percent >= 65 else
        "needs_practice"
    )

    return {
        "expected": expected_text,
        "spoken": spoken_text,
        "similarity_percent": similarity_percent,
        "verdict": verdict,
    }
