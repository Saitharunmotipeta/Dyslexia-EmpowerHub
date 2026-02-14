# app/feedback/services/pattern_service.py

import difflib


def detect_error_pattern(expected: str, spoken: str, content_type: str):
    spoken = (spoken or "").strip().lower()
    expected = (expected or "").strip().lower()

    # ----------------------------
    # 🚫 Silence
    # ----------------------------
    if spoken == "":
        return {
            "code": "silence",
            "message": "Nothing was detected in your speech.",
            "tip": "Check your mic and try speaking a little louder 🙂",
        }

    # ----------------------------
    # 🔤 WORD LEVEL PATTERNS
    # ----------------------------
    if content_type == "word":

        if len(spoken.split()) > 1:
            return {
                "code": "extra_words",
                "message": "You added extra words.",
                "tip": "Say only the target word — short and clear 🌟",
            }

        if spoken.endswith("uh"):
            return {
                "code": "trailing_vowel",
                "message": "You’re adding a small extra sound at the end.",
                "tip": "End the word cleanly — stop firmly 🔊",
            }

        if spoken and expected and spoken[0] != expected[0]:
            return {
                "code": "wrong_start_sound",
                "message": "The starting sound is different.",
                "tip": f"Focus on the first sound: '{expected[0]}'",
            }

        ratio = difflib.SequenceMatcher(None, expected, spoken).ratio()

        if ratio < 0.4:
            return {
                "code": "far_off",
                "message": "The pronunciation sounds quite different.",
                "tip": "Try saying it slowly — one sound at a time 🧩",
            }

    # ----------------------------
    # 📝 SENTENCE / PHRASE PATTERNS
    # ----------------------------
    if content_type in ["phrase", "sentence"]:

        expected_words = expected.split()
        spoken_words = spoken.split()

        missing = [w for w in expected_words if w not in spoken_words]
        extra = [w for w in spoken_words if w not in expected_words]

        if missing:
            return {
                "code": "missing_words",
                "message": "Some words were missed.",
                "tip": f"Focus on these words: {', '.join(missing)}",
            }

        if extra:
            return {
                "code": "extra_words_sentence",
                "message": "You added extra words.",
                "tip": "Try saying exactly what is written.",
            }

    # ----------------------------
    # ✅ Normal Case
    # ----------------------------
    return {
        "code": "normal",
        "message": "Your speech matches closely.",
        "tip": "Keep practicing for smoother fluency ✨",
    }
