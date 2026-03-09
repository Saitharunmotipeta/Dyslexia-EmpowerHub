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
    """
    Rough token estimation.
    Approx: 1 token ≈ 4 characters.
    """
    return max(1, len(text) // 4)


def call_llm(prompt: str) -> str:
    """
    Sends prompt to OpenRouter LLM and returns cleaned response.
    """

    estimated_input_tokens = estimate_tokens(prompt)

    if ENABLE_TOKEN_PRINT:
        print(f"[TOKEN DEBUG] Estimated input tokens: {estimated_input_tokens}")

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",

                # Recommended optional headers
                "HTTP-Referer": "http://localhost",
                "X-Title": "dyslexia-backend",
            },
            json={
                "model": MODEL_NAME,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": TEMPERATURE,
                "max_tokens": MAX_TOKENS,
            },
            timeout=20,
        )

        # Debug API errors
        if response.status_code != 200:
            print("[LLM ERROR] Status Code:", response.status_code)
            print("[LLM ERROR] Response:", response.text)
            raise Exception("OpenRouter API request failed")

        data = response.json()

        if "choices" not in data or not data["choices"]:
            print("[LLM ERROR] Invalid API response:", data)
            raise Exception("Malformed response from OpenRouter")

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

    except requests.exceptions.Timeout:
        print("[LLM ERROR] Request timed out")
        return "The assistant took too long to respond. Please try again."

    except requests.exceptions.RequestException as e:
        print(f"[LLM ERROR] Network error: {str(e)}")
        return "Network issue occurred while contacting the AI service."

    except Exception as e:
        print(f"[LLM ERROR] {str(e)}")
        return "You're making progress. Let's take the next small step together."