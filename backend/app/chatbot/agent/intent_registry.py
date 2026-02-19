# app/chatbot/agent/intent_registry.py

INTENT_MAP = {
    "resume_progress": {
        "engine": "resume_engine",
        "prompt": "resume.txt",
        "llm_required": True,
    },
    "level_completion": {
        "engine": "level_progress_engine",
        "prompt": None,
        "llm_required": False,
    },
    "feedback_analysis": {
        "engine": "word_similarity_engine",
        "prompt": "feedback.txt",
        "llm_required": True,
    },
    "performance_summary": {
        "engine": "aggregate_engine",
        "prompt": "progress.txt",
        "llm_required": True,
    },
    "learning_guidance": {
        "engine": None,
        "prompt": "guidance.txt",
        "llm_required": True,
    },
    "general": {
        "engine": None,
        "prompt": "general.txt",
        "llm_required": True,
    },
}
