# app/feedback/services/pattern_service.py

import difflib


def detect_error_pattern(
    expected: str,
    spoken: str,
    content_type: str,
    syllables: str | None = None,
    alignment=None,   # 🔥 NEW
):

    spoken = (spoken or "").strip().lower()
    expected = (expected or "").strip().lower()

    # -------------------------
    # SILENCE CHECK
    # -------------------------
    if spoken == "":
        return {
            "code": "silence",
            "message": "We couldn't detect any speech.",
            "tip": "Check your microphone and try speaking a little louder 🙂",
        }

    # -------------------------
    # WORD LOGIC (KEEP AS IS)
    # -------------------------
    if content_type == "word":

        if len(spoken.split()) > 1:
            return {
                "code": "extra_words",
                "message": "You added extra words.",
                "tip": "Try saying only the target word — short and clear.",
            }

        if spoken.endswith("uh") or spoken.endswith("a"):
            return {
                "code": "trailing_vowel",
                "message": "There may be a small extra sound at the end.",
                "tip": "Try ending the word a little more firmly.",
            }

        if spoken and expected and spoken[0] != expected[0]:
            return {
                "code": "wrong_start_sound",
                "message": "The starting sound was slightly different.",
                "tip": f"Focus on the first sound: '{expected[0]}'",
            }

        ratio = difflib.SequenceMatcher(None, expected, spoken).ratio()

        if ratio > 0.85:
            return {
                "code": "near_correct",
                "message": "Very close pronunciation!",
                "tip": "A small adjustment will make it perfect.",
            }

        if ratio > 0.65:
            return {
                "code": "minor_variation",
                "message": "Your pronunciation is close.",
                "tip": "Try speaking a little slower and emphasize each sound.",
            }

        if ratio > 0.45:
            return {
                "code": "noticeable_difference",
                "message": "Some sounds were different from the target word.",
                "tip": "Try breaking it into parts and speaking slowly.",
            }

        return {
            "code": "far_off",
            "message": "The pronunciation sounded quite different.",
            "tip": f"Try practicing slowly: {syllables.replace('-', ' • ') if syllables else 'one part at a time'}",
        }

    # -------------------------
    # 🔥 PHRASE / SENTENCE (UPGRADED)
    # -------------------------
    if content_type in ["phrase", "sentence"]:

        # 🔥 USE ALIGNMENT (NEW LOGIC)
        if alignment:
            types = [item["type"] for item in alignment]

            if "missing" in types:
                missing_words = [
                    item["expected"]
                    for item in alignment
                    if item["type"] == "missing"
                ]
                return {
                    "code": "missing_words",
                    "message": "Some words were skipped.",
                    "tip": f"Try including: {', '.join(missing_words)}",
                }

            if "extra" in types:
                return {
                    "code": "extra_words",
                    "message": "Some additional words were spoken.",
                    "tip": "Try saying exactly what is written.",
                }

            if "substitution" in types:
                return {
                    "code": "word_mismatch",
                    "message": "Some words were pronounced differently.",
                    "tip": "Focus on correcting the specific words.",
                }

            return {
                "code": "correct",
                "message": "The sentence was spoken correctly.",
                "tip": "Great job! Keep practicing for fluency.",
            }

        # -------------------------
        # FALLBACK (if no alignment)
        # -------------------------
        similarity = difflib.SequenceMatcher(None, expected, spoken).ratio()

        if similarity > 0.8:
            return {
                "code": "good_flow",
                "message": "The sentence was spoken smoothly.",
                "tip": "Keep practicing for natural rhythm.",
            }

        return {
            "code": "flow_difference",
            "message": "The sentence flow was a little different.",
            "tip": "Try speaking it slowly and clearly.",
        }

    # -------------------------
    # DEFAULT
    # -------------------------
    return {
        "code": "normal",
        "message": "Your speech matched closely.",
        "tip": "Keep practicing for smoother fluency ✨",
    }