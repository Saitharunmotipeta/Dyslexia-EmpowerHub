import re


def detect_intent(message: str) -> str:
    msg = message.lower()

    # -----------------------------
    # 1️⃣ Specific Last Activity Queries (STRICT FIRST)
    # -----------------------------
    if any(k in msg for k in [
        "last mock result",
        "last mock",
        "mock test result",
    ]):
        return "last_mock_result"

    if any(k in msg for k in [
        "last dynamic result",
        "last dynamic",
    ]):
        return "last_dynamic_result"

    if any(k in msg for k in [
        "which word did i practice",
        "what word did i practice",
        "last word practiced",
    ]):
        return "last_word_practice"

    # -----------------------------
    # 2️⃣ Resume / General Last Activity
    # -----------------------------
    if any(k in msg for k in [
        "where did i stop",
        "where i stopped",
        "resume",
        "continue",
        "last time",
        "yesterday",
        "last session",
    ]):
        return "resume_progress"
    
    # -----------------------------
    # Level Word Lookup
    # -----------------------------
    if (
        "level" in msg
        and any(k in msg for k in ["1st", "2nd", "3rd", "4th", "5th"])
    ):
        return "level_word_lookup"

    # -----------------------------
    # 3️⃣ Level Specific Queries
    # -----------------------------
    if any(k in msg for k in [
        "how many words",
        "words left",
        "words remaining",
        "how many left",
        "remaining words",
        "completion",
        "percent",
    ]):

        return "level_specific"

    # -----------------------------
    # 4️⃣ Practice Recommendation
    # -----------------------------
    if any(k in msg for k in [
        "what should i practice",
        "what next",
        "what now",
        "next step",
        "what to do next",
    ]):
        return "practice_recommendation"

    # -----------------------------
    # 5️⃣ Feedback / Pattern Analysis
    # -----------------------------
    if any(k in msg for k in [
        "mistake",
        "feedback",
        "analyze",
        "pattern",
        "why is my score low",
        "why am i struggling",
        "weak",
        "similarity",
    ]):
        return "feedback_analysis"

    # -----------------------------
    # 6️⃣ Performance Summary
    # -----------------------------
    if any(k in msg for k in [
        "score",
        "progress",
        "performance",
        "streak",
        "average",
        "am i improving",
        "overall performance",
    ]):
        return "performance_summary"

    # -----------------------------
    # 7️⃣ Learning Guidance
    # -----------------------------
    if any(k in msg for k in [
        "pronunciation",
        "reading",
        "dyslexia",
        "tips",
        "how to improve",
        "how do i improve",
    ]):
        return "learning_guidance"

    return "general"