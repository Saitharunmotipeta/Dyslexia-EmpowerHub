# app/chatbot/agent/orchestrator.py

from sqlalchemy.orm import Session

from app.chatbot.agent.intent_detector import detect_intent
from app.chatbot.agent.intent_registry import INTENT_MAP
from app.chatbot.agent.response_router import route_response

# Import ALL engines
from app.chatbot.analysis.resume_engine import run as resume_run
from app.chatbot.analysis.word_similarity_engine import run as similarity_run
from app.chatbot.analysis.aggregate_engine import run as aggregate_run
from app.chatbot.analysis.mock_engine import run as mock_run
from app.chatbot.analysis.level_progress_engine import run as level_progress_run
from app.chatbot.analysis.dynamic_engine import run as dynamic_run

ENGINE_MAP = {
    "resume_engine": resume_run,
    "level_progress_engine": level_progress_run,
    "word_similarity_engine": similarity_run,
    "aggregate_engine": aggregate_run,
    "mock_engine": mock_run,
    "dynamic_engine": dynamic_run,
}

def handle_chat(message: str, user_id: int, db: Session):

    # 1️⃣ Detect intent
    intent = detect_intent(message)

    intent_config = INTENT_MAP.get(intent)

    if not intent_config:
        return {
            "reply": "I’m here to help you move forward.",
            "mode": "general",
            "llm_used": False,
        }

    engine_name = intent_config.get("engine")
    prompt_file = intent_config.get("prompt")
    llm_required = intent_config.get("llm_required")

    structured_data = None

    # 2️⃣ Execute engine if defined
    if engine_name:
        engine_function = ENGINE_MAP.get(engine_name)

        if engine_function:
            structured_data = engine_function(
                user_id=user_id,
                db=db
            )

    # 3️⃣ Route response (deterministic OR LLM)
    reply, llm_used = route_response(
        intent=intent,
        structured_data=structured_data,
        prompt_file=prompt_file,
        message=message,
        llm_required=llm_required,
    )

    return {
        "reply": reply,
        "mode": intent,
        "llm_used": llm_used,
    }
