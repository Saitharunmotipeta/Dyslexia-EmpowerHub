def assert_not_empty(value, name="value"):
    if not value:
        raise AssertionError(f"[ASSERT FAIL] {name} is empty or missing")


def assert_status_code(resp, expected_code, context=""):
    if resp.status_code != expected_code:
        raise AssertionError(
            f"[ASSERT FAIL] {context}\n"
            f"Expected status {expected_code}, got {resp.status_code}\n"
            f"Response: {resp.text}"
        )
