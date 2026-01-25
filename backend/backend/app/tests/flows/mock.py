def run_mock_flow(client, context, cfg):
    """
    Run mock test end-to-end.
    """
    level_id = context["level_id"]

    # 1. Start mock
    resp = client.post("/mock/start", json={"level_id": level_id})
    if resp.status_code != 200:
        raise RuntimeError("Mock start failed")

    data = resp.json()
    attempt_id = data["attempt_id"]
    words = data["words"]

    # 2. Submit each word
    for w in words:
        word_id = w["id"]

        resp = client.post(
            "/mock/word",
            json={
                "attempt_id": attempt_id,
                "word_id": word_id
            }
        )
        if resp.status_code != 200:
            raise RuntimeError(f"Mock word failed for word_id={word_id}")

    # 3. Finish mock
    resp = client.post(
        "/mock/result",
        json={"attempt_id": attempt_id}
    )
    if resp.status_code != 200:
        raise RuntimeError("Mock result failed")

    result = resp.json()

    # 4. Download report
    resp = client.get(f"/mock/report?attempt_id={attempt_id}")
    if resp.status_code != 200:
        raise RuntimeError("Mock report download failed")

    return {
        "attempt_id": attempt_id,
        "mock_result": result,
        "report_bytes": len(resp.content)
    }
