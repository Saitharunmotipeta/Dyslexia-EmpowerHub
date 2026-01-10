def assert_practice_success(result: dict):
    if "practiced_words" not in result:
        raise AssertionError("[PRACTICE ASSERT] Missing practiced_words")

    if not isinstance(result["practiced_words"], list):
        raise AssertionError("[PRACTICE ASSERT] practiced_words must be a list")

    if len(result["practiced_words"]) == 0:
        raise AssertionError("[PRACTICE ASSERT] No practice attempts recorded")
