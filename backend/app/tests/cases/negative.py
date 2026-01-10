from asserts.common import assert_status_code


def run_negative_cases(client, context, cfg):
    """
    Negative / edge scenarios.
    """

    # -------------------------
    # INVALID MOCK START
    # -------------------------
    resp = client.post("/mock/start", json={"level_id": 999999})
    assert_status_code(resp, 404, "Invalid level_id for mock start")

    # -------------------------
    # INVALID MOCK RESULT
    # -------------------------
    resp = client.post("/mock/result", json={"attempt_id": 999999})
    assert_status_code(resp, 404, "Invalid attempt_id for mock result")

    # -------------------------
    # INVALID REPORT ACCESS
    # -------------------------
    resp = client.get("/mock/report?attempt_id=999999")
    assert_status_code(resp, 404, "Invalid report access")

    # -------------------------
    # PRACTICE WITH INVALID WORD
    # -------------------------
    resp = client.post(
        "/practice/evaluate",
        json={"word_id": 999999}
    )
    assert_status_code(resp, 404, "Practice with invalid word_id")

    # -------------------------
    # STT WITH INVALID / NOISE AUDIO
    # -------------------------
    invalid_audio = "tests/audio_samples/invalid/noise.wav"

    try:
        with open(invalid_audio, "rb") as f:
            resp = client.post(
                "/practice/upload",
                files={"file": f}
            )
    except FileNotFoundError:
        # Invalid audio not present → skip safely
        return

    if resp.status_code != 200:
        return  # backend rejected upload → acceptable

    file_id = resp.json().get("file_id")
    if not file_id:
        return

    client.post(f"/practice/convert/{file_id}")
    resp = client.post(f"/practice/stt/{file_id}")

    if resp.status_code not in (200, 400):
        raise AssertionError("STT invalid audio caused unexpected failure")
