# app/feedback/services/pattern_service.py

import difflib


def detect_error_pattern(expected: str, spoken: str):
    spoken = (spoken or "").strip().lower()
    expected = (expected or "").strip().lower()

    if spoken == "":
        return {
            "code": "silence",
            "title": "No Audio Detected",
            "message": "Looks like nothing was detected in your recording.",
            "tip": "Check your mic and try speaking a little louder 😄",
            "severity": "low"
        }

    if len(spoken.split()) > 1:
        return {
            "code": "extra_words",
            "title": "Extra Words Spoken",
            "message": "You added extra words while saying the target word.",
            "tip": "Try saying only the word — short and clear 🌟",
            "severity": "medium"
        }

    if spoken.endswith("uh"):
        return {
            "code": "trailing_vowel",
            "title": "Trailing Vowel Detected",
            "message": "You’re adding a small ‘uh’ sound at the end.",
            "tip": "End the word cleanly — like stopping a note 🎵",
            "severity": "medium"
        }

    if spoken and expected and spoken[0] != expected[0]:
        return {
            "code": "wrong_start_sound",
            "title": "Start Sound Mismatch",
            "message": "The first sound of the word doesn’t match.",
            "tip": f"Focus on the starting sound: '{expected[0]}' 🔊",
            "severity": "high"
        }

    ratio = difflib.SequenceMatcher(None, expected, spoken).ratio()

    if ratio < 0.4:
        return {
            "code": "far_off",
            "title": "Pronunciation Way Off",
            "message": "The spoken word sounds quite different from the target word.",
            "tip": "Try saying it slowly — one sound at a time 🧩",
            "severity": "high"
        }
    

    return {
        "code": "normal",
        "title": "Pronunciation Close",
        "message": "Your pronunciation is close to the target word!",
        "tip": "Keep polishing the small details ✨",
        "severity": "low"
    }
