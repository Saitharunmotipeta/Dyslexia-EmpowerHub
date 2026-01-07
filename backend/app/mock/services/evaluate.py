from difflib import SequenceMatcher


def evaluate_similarity(expected: str, spoken: str) -> dict:
    """
    Text-only evaluation (current phase)

    Returns:
      {
        score: float,
        verdict: str
      }
    """

    if not expected or not spoken:
        return {
            "score": 0.0,
            "verdict": "invalid_input"
        }

    ratio = SequenceMatcher(
        None,
        expected.lower().strip(),
        spoken.lower().strip()
    ).ratio()

    score = round(ratio * 100, 2)

    verdict = (
        "excellent" if score >= 85 else
        "good" if score >= 65 else
        "needs_practice"
    )

    return {
        "score": score,
        "verdict": verdict
    }
