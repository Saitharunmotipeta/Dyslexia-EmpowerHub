import os
import requests
import importlib.resources as pkg_resources

from app.dynamic.utils.ai_cache import meaning_cache
import app.prompts  # 👈 package import (important)

# ----------------------------
# Feature flag (AI ON / OFF)
# ----------------------------
AI_MEANING_ENABLED = os.getenv("AI_MEANING_ENABLED", "true").lower() == "true"

# ----------------------------
# OpenRouter configuration
# ----------------------------
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Cheap, fast, stable — perfect for meaning explanations
MODEL_NAME = "mistralai/mistral-7b-instruct"

if AI_MEANING_ENABLED and not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY not set but AI_MEANING_ENABLED=true")

# ----------------------------
# Load prompt template SAFELY
# ----------------------------
with pkg_resources.files(app.prompts).joinpath(
    "dynamic_meaning.txt"
).open("r", encoding="utf-8") as f:
    PROMPT_TEMPLATE = f.read()


# ----------------------------
# Helpers
# ----------------------------
def _normalize_cache_key(text: str) -> str:
    return text.lower().strip()


# ----------------------------
# Public function
# ----------------------------
def generate_meaning(text: str, text_type: str) -> str:
    """
    Generate dyslexia-friendly meaning.
    Uses OpenRouter only when needed.
    Backend-cached for token efficiency.
    """

    # 🔒 COST GUARD 1 — skip AI for single words
    if text_type == "word":
        return f"'{text}' is a word. Read it slowly and say it clearly."

    # 🔒 FEATURE FLAG — AI OFF
    if not AI_MEANING_ENABLED:
        print("⚠️ AI MEANING DISABLED — using fallback")
        return "This sentence explains an idea in a simple way."

    cache_key = _normalize_cache_key(text)

    # 🔒 COST GUARD 2 — backend cache
    cached = meaning_cache.get(cache_key)
    if cached:
        print("🟢 AI CACHE HIT — no API call")
        return cached

    print("🔵 AI CACHE MISS — calling OpenRouter")

    # 🔒 COMPRESSED PROMPT
    prompt = PROMPT_TEMPLATE.replace("{{TEXT}}", text)

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "temperature": 0.2,
        "max_tokens": 40,
    }

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "Dyslexia-EmpowerHub",
    }

    try:
        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload,
            timeout=15,
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

        # 📊 TOKEN ESTIMATION (approximate)
        prompt_tokens = len(prompt.split())
        output_tokens = len(meaning.split())
        print(
            f"📊 TOKEN ESTIMATE → prompt={prompt_tokens}, "
            f"output={output_tokens}, total={prompt_tokens + output_tokens}"
        )

        meaning_cache.set(cache_key, meaning)
        print("💾 AI CACHE STORED")

        return meaning

    except Exception as e:
        print("⚠️ OpenRouter meaning generation failed:", e)

        fallback = "This sentence explains an idea in a simple way."
        meaning_cache.set(cache_key, fallback)
        return fallback
