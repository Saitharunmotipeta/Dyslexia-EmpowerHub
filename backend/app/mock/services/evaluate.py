from difflib import SequenceMatcher

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
# PHONEME EXTRACTION
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
# CONFIDENCE LEVEL
# -----------------------------

def _confidence_level(score: float) -> str:

    if score >= 90:
        return "very_confident"

    if score >= 75:
        return "confident"

    if score >= 60:
        return "developing"

    return "needs_guidance"


# -----------------------------
# MAIN EVALUATION
# -----------------------------

def evaluate_similarity(expected: str, spoken: str) -> dict:
    """
    Pronunciation evaluation engine.
    Designed for dyslexia-friendly learning environments.
    """

    if not expected or not spoken:
        return {
            "score": 0.0,
            "verdict": "invalid_input",
            "confidence": "needs_guidance",
            "phonetics": {
                "expected": [],
                "recognized": [],
                "insights": {}
            },
            "feedback": [
                "No worries — let's try that again together.",
                "Speak slowly and comfortably 🌱"
            ],
            "practice_tip": "Take a deep breath and repeat the word slowly."
        }

    # -----------------------------
    # 1️⃣ Text Similarity Score
    # -----------------------------

    score = _text_similarity(expected, spoken)

    verdict = (
        "excellent" if score >= 90 else
        "good" if score >= 75 else
        "improving" if score >= 60 else
        "needs_practice"
    )

    confidence = _confidence_level(score)

    # -----------------------------
    # 2️⃣ Phoneme Analysis
    # -----------------------------

    expected_p = _extract_phonemes(expected)
    spoken_p = _extract_phonemes(spoken)

    insights = _compare_phonemes(expected_p, spoken_p)

    # -----------------------------
    # 3️⃣ Build Feedback
    # -----------------------------

    feedback_points = []

    if insights.get("initial_sound") == "mismatch":
        feedback_points.append(
            "Focus on the starting sound — begin the word clearly."
        )

    if insights.get("vowel") == "confusion":
        feedback_points.append(
            "The vowel sound can be improved. Slow down and listen to the middle sound."
        )

    if insights.get("final_sound") == "mismatch":
        feedback_points.append(
            "Try finishing the word fully without rushing the ending."
        )

    # -----------------------------
    # 4️⃣ Emotion-Aware Messaging
    # -----------------------------

    if verdict == "excellent":

        feedback_points.insert(
            0,
            "Beautiful pronunciation! 🌟 Clear and confident."
        )

    elif verdict == "good":

        feedback_points.insert(
            0,
            "Nice effort! You're very close 👍"
        )

    elif verdict == "improving":

        feedback_points.insert(
            0,
            "Good progress 💪 Your pronunciation is improving."
        )

    else:

        feedback_points.insert(
            0,
            "Good attempt — and every attempt helps your brain learn 🧠"
        )

    # -----------------------------
    # 5️⃣ Practice Tip
    # -----------------------------

    practice_tip = (
        "Try speaking the word slowly, one sound at a time."
        if verdict != "excellent"
        else "Keep practicing to build fluency."
    )

    return {
        "score": score,
        "verdict": verdict,
        "confidence": confidence,
        "phonetics": {
            "expected": expected_p,
            "recognized": spoken_p,
            "insights": insights
        },
        "feedback": feedback_points,
        "practice_tip": practice_tip
    }