import os
from app.chatbot.services.llm_client import call_llm
from app.learning.models.word import Word


# -------------------------
# LOAD PROMPT
# -------------------------
def load_prompt():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    path = os.path.join(base_dir, "prompts", "recommendation.txt")

    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def is_valid_word(word):
    # 🔥 simple validation: check if it's a single word and not empty
    return word.isalpha() and len(word) > 0


PROMPT_TEMPLATE = load_prompt()


# -------------------------
# WORD GENERATION ENGINE
# -------------------------
def generate_similar_words(expected: str, spoken: str, pattern: dict | None):

    if not expected:
        return []

    try:
        issue = pattern.get("code") if pattern else "unknown"

        prompt = PROMPT_TEMPLATE.format(
            expected=expected,
            spoken=spoken,
            issue=issue
        )

        response = call_llm(prompt)

        if not response:
            raise Exception("Empty LLM response")

        # -------------------------
        # CLEAN OUTPUT
        # -------------------------

        words = [
            w.strip().lower()
            for w in response.replace("\n", ",").split(",")
                 if is_valid_word(w.strip())
        ]
        if not words:
            return []

        # 🔥 remove duplicates + limit
        words = list(dict.fromkeys(words))[:3]

        return words

    except Exception as e:
        return []