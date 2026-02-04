# app/practice/services/stt_service.py

"""
Browser-based STT service.

Speech recognition is done on the client (browser).
Backend receives recognized text directly.
"""


def speech_to_text_from_browser(text: str) -> dict:
    """
    Accepts already-recognized speech text from browser.
    """

    if not text or not text.strip():
        return {
            "text": "",
            "confidence": 0.0,
            "source": "browser",
        }

    return {
        "text": text.strip().lower(),
        "confidence": 1.0,
        "source": "browser",
    }
