def assert_mock_success(result: dict):
    # attempt_id
    if "attempt_id" not in result:
        raise AssertionError("[MOCK ASSERT] Missing attempt_id")

    # result object
    mock_result = result.get("mock_result")
    if not mock_result:
        raise AssertionError("[MOCK ASSERT] Missing mock_result")

    # score
    score = mock_result.get("score")
    if score is None:
        raise AssertionError("[MOCK ASSERT] Missing score")

    if not (0 <= score <= 100):
        raise AssertionError(f"[MOCK ASSERT] Invalid score value: {score}")

    # verdict
    verdict = mock_result.get("verdict")
    if verdict not in ("excellent", "good_progress", "keep_practicing", "good"):
        raise AssertionError(f"[MOCK ASSERT] Unexpected verdict: {verdict}")

    # words
    words = mock_result.get("words")
    if not words or not isinstance(words, list):
        raise AssertionError("[MOCK ASSERT] Words list missing or invalid")

    # confidence
    confidence = mock_result.get("confidence")
    if confidence is not None and not (0 <= confidence <= 1):
        raise AssertionError(f"[MOCK ASSERT] Invalid confidence: {confidence}")
