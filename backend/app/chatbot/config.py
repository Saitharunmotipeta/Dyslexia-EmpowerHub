import os


def get_bool(value: str, default: bool) -> bool:
    if value is None:
        return default
    return value.lower() in ("true", "1", "yes")


def get_int(value: str, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def get_float(value: str, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


# ===== Feature Toggles =====

USE_LLM_FOR_NUMERIC = get_bool(
    os.getenv("CHATBOT_USE_LLM_FOR_NUMERIC"),
    False,
)

ENABLE_TOKEN_PRINT = get_bool(
    os.getenv("CHATBOT_ENABLE_TOKEN_PRINT"),
    True,
)

# ===== Limits =====

MAX_RESPONSE_LINES = get_int(
    os.getenv("CHATBOT_MAX_RESPONSE_LINES"),
    8,
)

MAX_PROMPT_CHAR_LENGTH = get_int(
    os.getenv("CHATBOT_MAX_PROMPT_CHAR_LENGTH"),
    2000,
)

# ===== Model Config =====

MODEL_NAME = os.getenv(
    "CHATBOT_MODEL_NAME",
    "mistralai/mistral-7b-instruct",
)

TEMPERATURE = get_float(
    os.getenv("CHATBOT_TEMPERATURE"),
    0.6,
)

MAX_TOKENS = get_int(
    os.getenv("CHATBOT_MAX_TOKENS"),
    300,
)
