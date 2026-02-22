# app/chatbot/agent/intent_registry.py

INTENT_MAP = {

    # -----------------------------
    # Specific Last Activity
    # -----------------------------
    "last_mock_result": {
        "engine": "mock_engine",
        "prompt": "resume.txt",
        "llm_required": True,
    },

    "last_dynamic_result": {
        "engine": "dynamic_engine",
        "prompt": "resume.txt",
        "llm_required": True,
    },

    "last_word_practice": {
        "engine": "last_word_engine",
        "prompt": "resume.txt",
        "llm_required": True,
    },

    # -----------------------------
    # Resume / General Last Activity
    # -----------------------------
    "resume_progress": {
        "engine": "resume_engine",
        "prompt": "resume.txt",
        "llm_required": True,
    },

    # -----------------------------
    # Level Specific Queries
    # -----------------------------
    "level_specific": {
        "engine": "level_progress_engine",
        "prompt": None,
        "llm_required": False,
    },

    # -----------------------------
    # Practice Recommendation
    # -----------------------------
    "practice_recommendation": {
        "engine": "level_progress_engine",
        "prompt": None,
        "llm_required": False,
    },

    # -----------------------------
    # Feedback / Pattern Analysis
    # -----------------------------
    "feedback_analysis": {
        "engine": "word_similarity_engine",
        "prompt": "feedback.txt",
        "llm_required": True,
    },

    # -----------------------------
    # Performance Summary
    # -----------------------------
    "performance_summary": {
        "engine": "aggregate_engine",
        "prompt": "progress.txt",
        "llm_required": True,
    },

    # -----------------------------
    # Learning Guidance
    # -----------------------------
    "learning_guidance": {
        "engine": None,
        "prompt": "guidance.txt",
        "llm_required": True,
    },

    # -----------------------------
    # General
    # -----------------------------
    "general": {
        "engine": None,
        "prompt": "general.txt",
        "llm_required": True,
    },

    "level_word_lookup": {
        "engine": "level_word_lookup_engine",
        "prompt": "word_lookup.txt",
        "llm_required": True,
    },
}