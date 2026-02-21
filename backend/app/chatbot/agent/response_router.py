from app.chatbot.services.prompt_loader import load_prompt
from app.chatbot.services.llm_client import call_llm
from app.chatbot.config import USE_LLM_FOR_NUMERIC


def route_response(
    intent: str,
    structured_data: dict | None,
    prompt_file: str | None,
    message: str,
    llm_required: bool,
):

    # ----------------------------
    # 1️⃣ Deterministic Bypass
    # ----------------------------
    if not llm_required or (
        not USE_LLM_FOR_NUMERIC and intent == "level_completion"
    ):
        if structured_data:
            return format_deterministic(intent, structured_data), False

    # ----------------------------
    # 2️⃣ Safe Prompt Handling
    # ----------------------------
    if not prompt_file:
        # If LLM required but no prompt defined
        return "I'm here to help you move forward step by step.", False

    # ----------------------------
    # 3️⃣ LLM Path
    # ----------------------------
    prompt_template = load_prompt(prompt_file)

    final_prompt = build_prompt(
        template=prompt_template,
        structured_data=structured_data,
        user_message=message,
    )

    reply = call_llm(final_prompt)

    return reply, True

def build_prompt(template: str, structured_data: dict | None, user_message: str):

    context_block = ""

    if structured_data:

        bullet_lines = []

        for key, value in structured_data.items():

            if isinstance(value, dict):
                for sub_key, sub_val in value.items():
                    bullet_lines.append(f"- {sub_key}: {sub_val}")
            else:
                bullet_lines.append(f"- {key}: {value}")

        context_block = "\nUser Facts:\n" + "\n".join(bullet_lines) + "\n"

    return (
        f"{template}\n"
        f"{context_block}\n"
        f"User Question:\n{user_message}"
    )


# -------------------------------------------------------
# DETERMINISTIC RESPONSES (No LLM)
# -------------------------------------------------------

def format_deterministic(intent: str, data: dict) -> str:

    # -----------------------------------------
    # Level Specific & Practice Recommendation
    # -----------------------------------------
    if intent in ["level_specific", "practice_recommendation"]:

        return (
            f"Level: {data.get('level_name')}\n"
            f"Total words: {data.get('total_words')}\n"
            f"Mastered: {data.get('mastered_words')}\n"
            f"Attempted: {data.get('attempted_words')}\n"
            f"Remaining: {data.get('remaining_words')}\n"
            f"Completion: {data.get('completion_percent')}%\n"
            f"Recommendation: {data.get('recommendation')}"
        )

    # -----------------------------------------
    # Performance Summary
    # -----------------------------------------
    if intent == "performance_summary":

        return (
            f"Mock Average: {data.get('mock_average')}\n"
            f"Dynamic Average: {data.get('dynamic_average')}\n"
            f"Similarity Average: {data.get('similarity_average')}"
        )

    # -----------------------------------------
    # Fallback (Should Rarely Trigger)
    # -----------------------------------------
    return "You're progressing steadily. Keep going."

    if intent == "level_completion":
        total = data.get("total_words", 0)
        attempted = data.get("attempted_words", 0)
        mastered = data.get("mastered_words", 0)
        percent = data.get("completion_percent", 0)

        remaining = total - mastered if total else 0

        return (
            f"You have completed {percent}% of this level.\n"
            f"Words mastered: {mastered} out of {total}.\n"
            f"Words attempted: {attempted}.\n"
            f"Remaining words: {remaining}."
        )

    if intent == "performance_summary":
        mock_avg = data.get("mock_average")
        dynamic_avg = data.get("dynamic_average")
        similarity_avg = data.get("similarity_average")

        return (
            f"Mock Average: {mock_avg}\n"
            f"Dynamic Average: {dynamic_avg}\n"
            f"Similarity Average: {similarity_avg}"
        )

    return "You're progressing steadily. Keep going."