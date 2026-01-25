"""
Mock STT expectations for deterministic testing.
These are NOT injected into backend — they are
used to validate responses after /practice/stt.
"""

MOCK_STT_OUTPUTS = {
    # word_id : expected recognized text
    1: "cat",
    2: "dog",
    3: "tree",
    4: "apple",
    5: "ball",
}
