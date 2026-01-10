"""
Negative / edge STT outputs.
Used to validate robustness.
"""

INVALID_STT_CASES = {
    "empty_audio": "",
    "noise_only": "zzz zzz",
    "wrong_language": "hola",
    "garbage": "@@@ ### !!!"
}
