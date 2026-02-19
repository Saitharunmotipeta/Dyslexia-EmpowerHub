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

    # Deterministic numeric bypass
    if not llm_required or (not USE_LLM_FOR_NUMERIC and intent == "level_completion"):
        if structured_data:
            return format_deterministic(intent, structured_data), False

    # If no prompt file but LLM required, fallback safely
    if not prompt_file:
        return "I'm here to help you improve step by step.", False

    # LLM path
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
        context_lines = "\n".join(
            [f"{k}: {v}" for k, v in structured_data.items()]
        )
        context_block = f"\nUser Data:\n{context_lines}\n"

    return f"{template}\n{context_block}\nUser Question:\n{user_message}"


def format_deterministic(intent: str, data: dict) -> str:

    if intent == "level_completion":
        return (
            f"You have completed {data.get('completion_percent')}% "
            f"of Level {data.get('level_id')}.\n"
            f"Words attempted: {data.get('attempted_words')} "
            f"out of {data.get('total_words')}."
        )

    if intent == "performance_summary":
        return (
            f"Mock Average: {data.get('mock_average')}\n"
            f"Dynamic Average: {data.get('dynamic_average')}."
        )

    return "You're progressing steadily. Keep going."
