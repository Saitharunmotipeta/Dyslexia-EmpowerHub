from app.core.paths import STT_ENGINE, TTS_ENGINE, IS_DEV


def initialize_media_layer():
    """
    Initializes media configuration.
    Safe to extend later when Deepgram is integrated.
    """

    if IS_DEV:
        print("🔧 Media Layer Bootstrapping...")
        print(f"🗣️ STT Engine  → {STT_ENGINE}")
        print(f"🔊 TTS Engine  → {TTS_ENGINE}")

    # Future: Validate Deepgram config
    if STT_ENGINE == "deepgram":
        print("🌐 Deepgram STT mode enabled")

    if TTS_ENGINE == "external":
        print("🌐 External TTS mode enabled")