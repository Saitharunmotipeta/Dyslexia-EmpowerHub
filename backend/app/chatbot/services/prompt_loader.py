# app/chatbot/services/prompt_loader.py

import os


PROMPT_BASE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "prompts",
    "chatbot"
)

def load_prompt(filename: str) -> str:
    path = os.path.join(PROMPT_BASE_PATH, filename)

    if not os.path.exists(path):
        raise FileNotFoundError(f"Prompt file not found: {filename}")

    with open(path, "r", encoding="utf-8") as file:
        return file.read()
