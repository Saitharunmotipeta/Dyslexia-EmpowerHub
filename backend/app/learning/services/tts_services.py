# app/learning/services/tts_services.py

PACE_TO_RATE = {
    "slow": 0.75,
    "medium": 1.0,
    "fast": 1.25,
}


def prepare_browser_tts(
    text: str,
    pace: str = "medium",
) -> dict:
    """
    Returns metadata for browser-based TTS.
    No audio generation happens here.
    """

    rate = PACE_TO_RATE.get(pace, 1.0)

    return {
        "engine": "browser",
        "text": text,
        "rate": rate,
        "language": "en-US",
        "hint": "Use SpeechSynthesisUtterance",
    }
