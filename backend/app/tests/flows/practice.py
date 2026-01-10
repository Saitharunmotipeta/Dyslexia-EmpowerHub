import os

AUDIO_DIR = "tests/audio_samples"


def run_practice_flow(client, context, cfg):
    """
    Simulate practice flow for enough words
    to build mastery.
    """
    word_ids = context["word_ids"]
    practiced = []

    for word_id in word_ids:
        audio_path = _select_audio(word_id, cfg)

        # STEP 1: upload
        with open(audio_path, "rb") as f:
            resp = client.post(
                "/practice/upload",
                files={"file": f}
            )
        if resp.status_code != 200:
            raise RuntimeError("Upload failed")

        file_id = resp.json().get("file_id")
        if not file_id:
            raise RuntimeError("Upload response missing file_id")

        # STEP 2: convert
        resp = client.post(f"/practice/convert/{file_id}")
        if resp.status_code != 200:
            raise RuntimeError("Convert failed")

        # STEP 3: stt
        resp = client.post(f"/practice/stt/{file_id}")
        if resp.status_code != 200:
            raise RuntimeError("STT failed")

        stt_data = resp.json()
        recognized_text = (
            stt_data.get("recognized_text")
            or stt_data.get("text")
        )

        if not recognized_text:
            raise RuntimeError("STT returned empty recognized text")

        # STEP 4: evaluate
        resp = client.post(
            "/practice/evaluate",
            json={
                "word_id": word_id
            }
        )
        if resp.status_code != 200:
            raise RuntimeError("Evaluate failed")

        practiced.append(word_id)

    return {
        "practiced_words": practiced
    }


def _select_audio(word_id: int, cfg):
    """
    Select mock or real audio.
    """
    if cfg["USE_REAL_AUDIO"]:
        return f"{AUDIO_DIR}/real/{word_id}.wav"

    return f"{AUDIO_DIR}/mock/{word_id}.wav"
