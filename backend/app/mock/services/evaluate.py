from difflib import SequenceMatcher

# Safe phoneme import
try:
    from app.practice.services.phoneme_service import extract_phonemes as get_phonemes
except Exception:
    get_phonemes = None


VOWELS = {"AA", "AE", "AH", "EH", "IH", "IY", "UH", "UW"}


# -----------------------------
# TEXT SIMILARITY
# -----------------------------

def _text_similarity(expected: str, spoken: str) -> float:
    return round(
        SequenceMatcher(
            None,
            expected.lower().strip(),
            spoken.lower().strip()
        ).ratio() * 100,
        2
    )


# -----------------------------
# PHONEME EXTRACTION (SAFE)
# -----------------------------

def _extract_phonemes(word: str):
    if not get_phonemes or not word:
        return []

    try:
        result = get_phonemes(word)
        return result if isinstance(result, list) else []
    except Exception:
        return []


# -----------------------------
# PHONEME COMPARISON
# -----------------------------

def _compare_phonemes(expected_p, spoken_p):
    insights = {
        "initial_sound": "unknown",
        "vowel": "unknown",
        "final_sound": "unknown"
    }

    if not expected_p or not spoken_p:
        return insights

    insights["initial_sound"] = (
        "correct" if expected_p[0] == spoken_p[0] else "mismatch"
    )

    insights["final_sound"] = (
        "correct" if expected_p[-1] == spoken_p[-1] else "mismatch"
    )

    expected_vowels = [p for p in expected_p if p in VOWELS]
    spoken_vowels = [p for p in spoken_p if p in VOWELS]

    insights["vowel"] = (
        "correct" if expected_vowels == spoken_vowels else "confusion"
    )

    return insights


# -----------------------------
# MAIN EVALUATION
# -----------------------------

def evaluate_similarity(expected: str, spoken: str) -> dict:
    """
    Production-grade pronunciation evaluation.
    Emotionally supportive. Analytically reliable.
    """

    if not expected or not spoken:
        return {
            "score": 0.0,
            "verdict": "invalid_input",
            "phonetics": {
                "expected": [],
                "recognized": [],
                "insights": {}
            },
            "feedback": (
                "No worries — let’s try that again together, "
                "slowly and comfortably 🌱"
            )
        }

    # 1️⃣ Text similarity
    score = _text_similarity(expected, spoken)

    verdict = (
        "excellent" if score >= 85 else
        "good" if score >= 65 else
        "needs_practice"
    )

    # 2️⃣ Phoneme analysis
    expected_p = _extract_phonemes(expected)
    spoken_p = _extract_phonemes(spoken)

    insights = _compare_phonemes(expected_p, spoken_p)

    # 3️⃣ Intelligent feedback construction
    feedback_points = []

    if insights.get("initial_sound") == "mismatch":
        feedback_points.append(
            "Pay attention to the starting sound — begin it more clearly."
        )

    if insights.get("vowel") == "confusion":
        feedback_points.append(
            "The vowel sound needs a bit of tuning. Slow down and feel the sound."
        )

    if insights.get("final_sound") == "mismatch":
        feedback_points.append(
            "Try to finish the word fully — don’t rush the ending."
        )

    # 4️⃣ Emotion-aware messaging
    if verdict == "excellent":
        feedback = (
            "That was beautifully pronounced! 🌟 "
            "Clear, confident, and well done."
        )

    elif verdict == "good":
        feedback = (
            "Nice effort! 👍 You’re very close. "
            + (" ".join(feedback_points) if feedback_points else
               "With a bit more practice, you’ll get it perfectly.")
        )

    else:
        feedback = (
            "Good try — and that effort matters 💪 "
            + (" ".join(feedback_points) if feedback_points else
               "Take your time and try again.")
            + " Every attempt helps your brain learn."
        )

    return {
        "score": score,
        "verdict": verdict,
        "phonetics": {
            "expected": expected_p,
            "recognized": spoken_p,
            "insights": insights
        },
        "feedback": feedback
    }
