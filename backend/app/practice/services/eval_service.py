from difflib import SequenceMatcher


def evaluate_similarity(expected_text: str, spoken_text: str) -> tuple[float, str]:
    """
    Returns:
      score_percent, verdict
    """

    print("🔍 Checking inputs...")
    if not expected_text or not spoken_text:
        print("⚠️ Invalid input detected: expected_text='", expected_text, "', spoken_text='", spoken_text, "'")
        return 0.0, "invalid_input"

    print("✅ Inputs are valid. Calculating similarity...")
    ratio = SequenceMatcher(
        None,
        expected_text.lower().strip(),
        spoken_text.lower().strip()
    ).ratio()

    print(f"🔢 Similarity ratio calculated: {ratio}")
    score = round(ratio * 100, 2)
    print(f"📊 Score (percentage): {score}%")

    verdict = (
        "excellent" if score >= 85 else
        "good" if score >= 65 else
        "needs_practice"
    )

    print(f"📝 Verdict: {verdict}")
    return score, verdict
