from pathlib import Path


def run_practice_flow(client, context, cfg):
    """
    Simulate practice flow for enough words
    to build mastery.
    """

    # --------------------------------------------------
    # Resolve paths RELATIVE TO THIS FILE (CORRECT WAY)
    # --------------------------------------------------
    TESTS_DIR = Path(__file__).resolve().parents[1]   # app/tests
    AUDIO_SAMPLES_DIR = TESTS_DIR / "audio_samples"
    MOCK_AUDIO_DIR = AUDIO_SAMPLES_DIR / "mock"

    word_ids = context["word_ids"]
    practiced = []

    headers = {
        "Authorization": f"Bearer {client.token}"
    }

    print("🔎 CWD =", Path.cwd())
    print("🔎 MOCK_AUDIO_DIR =", MOCK_AUDIO_DIR)
    print("🔎 Exists =", MOCK_AUDIO_DIR.exists())

    for word_id in word_ids:
        audio_path = MOCK_AUDIO_DIR / f"{word_id}.wav"

        if not audio_path.exists():
            raise FileNotFoundError(
                f"Missing mock audio file: {audio_path}"
            )

        # --------------------
        # STEP 1: UPLOAD
        # --------------------
        with open(audio_path, "rb") as f:
            resp = client.post(
                "/practice/upload",
                files={"file": f},
                headers=headers
            )

        if resp.status_code != 200:
            raise RuntimeError(
                f"Upload failed ({resp.status_code}): {resp.text}"
            )

        file_id = resp.json().get("file_id")
        if not file_id:
            raise RuntimeError("Upload response missing file_id")

        # --------------------
        # STEP 2: CONVERT
        # --------------------
        resp = client.post(
            f"/practice/convert/{file_id}",
            headers=headers
        )

        if resp.status_code != 200:
            raise RuntimeError(
                f"Convert failed ({resp.status_code}): {resp.text}"
            )

        # --------------------
        # STEP 3: STT
        # --------------------
        resp = client.post(
            f"/practice/stt/{file_id}",
            headers=headers
        )

        if resp.status_code != 200:
            raise RuntimeError(
                f"STT failed ({resp.status_code}): {resp.text}"
            )

        stt_data = resp.json()
        recognized_text = (
            stt_data.get("recognized_text")
            or stt_data.get("text")
        )

        if not recognized_text:
            raise RuntimeError("STT returned empty recognized text")

        # --------------------
        # STEP 4: EVALUATE
        # --------------------
        resp = client.post(
            "/practice/evaluate",
            json={"word_id": word_id},
            headers=headers
        )

        if resp.status_code != 200:
            raise RuntimeError(
                f"Evaluate failed ({resp.status_code}): {resp.text}"
            )

        practiced.append(word_id)

    return {
        "practiced_words": practiced
    }
