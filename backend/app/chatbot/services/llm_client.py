import requests
import os

from app.chatbot.config import (
    MODEL_NAME,
    TEMPERATURE,
    MAX_TOKENS,
    MAX_RESPONSE_LINES,
    ENABLE_TOKEN_PRINT,
)


OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY is not set in environment variables.")


def estimate_tokens(text: str) -> int:
    return len(text) // 4  # rough estimate


def call_llm(prompt: str) -> str:

    estimated_input_tokens = estimate_tokens(prompt)

    if ENABLE_TOKEN_PRINT:
        print(f"[TOKEN DEBUG] Estimated input tokens: {estimated_input_tokens}")

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": MODEL_NAME,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": TEMPERATURE,
                "max_tokens": MAX_TOKENS,
            },
            timeout=20,
        )

        response.raise_for_status()
        data = response.json()

        content = data["choices"][0]["message"]["content"].strip()

        # Limit output lines
        lines = content.split("\n")
        final_output = "\n".join(lines[:MAX_RESPONSE_LINES]).strip()

        if ENABLE_TOKEN_PRINT:
            estimated_output_tokens = estimate_tokens(final_output)
            print(f"[TOKEN DEBUG] Estimated output tokens: {estimated_output_tokens}")
            print(
                f"[TOKEN DEBUG] Estimated total tokens: "
                f"{estimated_input_tokens + estimated_output_tokens}"
            )

        return final_output

    except Exception as e:
        print(f"[LLM ERROR] {str(e)}")
        return "You're making progress. Let's take the next small step together."
