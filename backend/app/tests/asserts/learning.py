def assert_learning_success(result: dict):
    if "learned_words" not in result:
        raise AssertionError("[LEARNING ASSERT] Missing learned_words")

    if not isinstance(result["learned_words"], list):
        raise AssertionError("[LEARNING ASSERT] learned_words must be a list")

    if len(result["learned_words"]) == 0:
        raise AssertionError("[LEARNING ASSERT] No words were learned")
