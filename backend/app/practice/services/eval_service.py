from difflib import SequenceMatcher


def evaluate_similarity(expected_text: str, spoken_text: str) -> tuple[float, str]:
    """
    Returns:
      score_percent, verdict
    """

    if not expected_text or not spoken_text:
        return 0.0, "invalid_input"

    ratio = SequenceMatcher(
        None,
        expected_text.lower().strip(),
        spoken_text.lower().strip()
    ).ratio()

    score = round(ratio * 100, 2)

    verdict = (
        "excellent" if score >= 85 else
        "good" if score >= 65 else
        "needs_practice"
    )

    return score, verdict
