def detect_intent(message: str) -> str:
    msg = message.lower()

    # Resume intent
    if any(k in msg for k in [
        "where did i stop",
        "resume",
        "continue",
        "last time",
        "yesterday",
        "last session",
    ]):
        return "resume_progress"

    # Level completion intent
    if any(k in msg for k in [
        "completion",
        "finished level",
        "completed level",
        "mastered",
        "percent completed",
    ]):
        return "level_completion"

    # Feedback / similarity analysis
    if any(k in msg for k in [
        "mistake",
        "feedback",
        "analyze",
        "pattern",
        "weak",
        "similarity",
    ]):
        return "feedback_analysis"

    # Performance summary
    if any(k in msg for k in [
        "score",
        "progress",
        "performance",
        "streak",
        "average",
        "improving",
    ]):
        return "performance_summary"

    # Learning guidance
    if any(k in msg for k in [
        "pronunciation",
        "reading",
        "dyslexia",
        "tips",
        "how to improve",
    ]):
        return "learning_guidance"

    return "general"
