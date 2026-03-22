import os
from app.chatbot.services.llm_client import call_llm


# -------------------------
# PROMPT LOADER
# -------------------------
def load_prompt():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    path = os.path.join(base_dir, "prompts", "feedback_rag.txt")

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


PROMPT_TEMPLATE = load_prompt()


# -------------------------
# SOUND GROUPS (LIGHT GUIDE)
# -------------------------
SOUND_GROUPS = {
    "th": ["th"],
    "f": ["f", "ph"],
    "k": ["k", "c", "q"],
    "s": ["s", "c", "z"],
    "b": ["b", "p"],
    "d": ["d", "t"],
    "g": ["g", "j"],
    "ch": ["ch", "tch"],
    "sh": ["sh"],
}


def extract_sound_units(word: str):
    word = word.lower()
    units = []
    i = 0

    while i < len(word):
        if i + 1 < len(word) and word[i:i+2] in ["th", "ph", "ch", "sh"]:
            units.append(word[i:i+2])
            i += 2
        else:
            units.append(word[i])
            i += 1

    return units


def normalize_sound(unit: str):
    for sound, variants in SOUND_GROUPS.items():
        if unit in variants:
            return sound
    return unit


# -------------------------
# LIGHT HINT ENGINE (GUIDE ONLY)
# -------------------------
def basic_sound_hint(expected: str, spoken: str):
    exp_words = expected.lower().split()
    spk_words = spoken.lower().split()

    # word split detection
    if len(spk_words) > len(exp_words):
        return "word split into parts"

    if len(spk_words) < len(exp_words):
        return "missing part of word"

    # phoneme-level mismatch
    for w_idx in range(len(exp_words)):
        exp_units = extract_sound_units(exp_words[w_idx])
        spk_units = extract_sound_units(spk_words[w_idx])

        for i in range(min(len(exp_units), len(spk_units))):
            exp = normalize_sound(exp_units[i])
            spk = normalize_sound(spk_units[i])

            if exp != spk:
                return f"'{spk_units[i]}' instead of '{exp_units[i]}'"

    return "minor pronunciation difference"


# -------------------------
# TOKEN ESTIMATION (ROUGH)
# -------------------------
def estimate_tokens(text: str):
    return int(len(text.split()) * 1.3)


# -------------------------
# MAIN AI REASONING ENGINE
# -------------------------
def generate_reasoning(expected: str, spoken: str, pattern: dict | None):
    """
    AI-powered pronunciation reasoning (RAG-lite + guided)
    """

    if not spoken or not spoken.strip():
        return "We couldn’t detect your speech. Try speaking clearly 🙂"

    try:
        # 🔹 generate hint (NOT final output)
        hint = basic_sound_hint(expected, spoken)

        # 🔹 build prompt (AI-focused)
        prompt = PROMPT_TEMPLATE.format(
            expected=expected,
            spoken=spoken
        )

        # -------------------------
        # TOKEN DEBUG
        # -------------------------
        input_tokens = estimate_tokens(prompt)

        print("----- RAG DEBUG -----")
        print("PROMPT:\n", prompt)
        print(f"[TOKEN DEBUG] Estimated input tokens: {input_tokens}")

        # 🔹 LLM CALL
        response = call_llm(prompt)

        output_tokens = estimate_tokens(response if response else "")

        print(f"[TOKEN DEBUG] Estimated output tokens: {output_tokens}")
        print(f"[TOKEN DEBUG] Estimated total tokens: {input_tokens + output_tokens}")
        print("LLM RESPONSE:", response)
        print("---------------------")

        if not response:
            raise Exception("Empty LLM response")

        # 🔴 FILTER BAD RESPONSES
        bad_keywords = ["spell", "type", "spelling", "typed"]

        if any(word in response.lower() for word in bad_keywords):
            return f"You said '{spoken}' instead of '{expected}'. Try saying it slowly and clearly."

        return response.strip()

    except Exception as e:
        print("❌ RAG ERROR:", str(e))
        return "Try saying it slowly and clearly. You're improving 👍"


# -------------------------
# TEST
# -------------------------
if __name__ == "__main__":
    print(generate_reasoning("competition", "sompet nation", None))