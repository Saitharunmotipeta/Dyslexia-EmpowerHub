import os
from pathlib import Path
import requests

# ----------------------------
# OpenRouter configuration
# ----------------------------
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY not set in environment")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Choose a reliable, cheap, stable model
# (Good for short explanations, not hallucination-heavy)
MODEL_NAME = "mistralai/mistral-7b-instruct"

# ----------------------------
# Load prompt template ONCE
# app/prompts/dynamic_learning/meaning.txt
# ----------------------------
PROMPT_PATH = (
    Path(__file__).resolve().parents[3]
    / "prompts"
    / "dynamic_meaning.txt"
)

with open(PROMPT_PATH, "r", encoding="utf-8") as f:
    PROMPT_TEMPLATE = f.read()


# ----------------------------
# Public function
# ----------------------------
def generate_meaning(text: str, text_type: str) -> str:
    """
    Generate dyslexia-friendly meaning.
    Uses OpenRouter only when needed.
    """

    # 🔒 Cost + latency guard
    if text_type == "word":
        return f"This word talks about '{text}'."

    prompt = PROMPT_TEMPLATE.replace("{{TEXT}}", text)

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You explain things for dyslexic learners. "
                    "Use short sentences. Simple words. Calm tone."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "temperature": 0.2,
        "max_tokens": 80,
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        # optional but recommended by OpenRouter
        "HTTP-Referer": "http://localhost",
        "X-Title": "Dyslexia-EmpowerHub",
    }

    try:
        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload,
            timeout=20,
        )
        response.raise_for_status()

        data = response.json()
        meaning = (
            data.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
            .strip()
        )

        if not meaning:
            raise ValueError("Empty response from OpenRouter")

        return meaning

    except Exception as e:
        # 🧠 Never break the user experience
        print("⚠️ OpenRouter meaning generation failed:", e)
        return (
            "This sentence explains an idea. "
            "Read it slowly. Focus on the main words."
        )

    finally:
        print("🧠 OpenRouter meaning generation attempted.")
