from app.insights.schemas import FeedbackIn, FeedbackOut
from app.insights.services.trends import trend_analysis
from app.insights.services.pattern_service import detect_error_pattern
from app.insights.services.rag_service import generate_reasoning


# 🔥 RESPONSE CLEANER (DYSLEXIA FRIENDLY)
def clean_response(text: str) -> str:
    if not text:
        return ""

    # 🔥 remove empty lines
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    # 🔥 remove useless starter lines
    filtered = []
    for line in lines:
        if "let's fix" in line.lower():
            continue
        filtered.append(line)

    # 🔥 keep only meaningful lines
    clean_lines = []
    for line in filtered[:2]:
        words = line.split()[:30]
        clean_lines.append(" ".join(words))

    return "\n".join(clean_lines)

# 🔥 SAFETY FILTER
def is_bad_response(text: str) -> bool:
    if not text:
        return True

    bad_keywords = ["spell", "letter", "typed", "spelling"]

    return any(word in text.lower() for word in bad_keywords)


def generate_feedback(data: FeedbackIn) -> FeedbackOut:

    score = data.score
    attempts = data.attempts
    content_type = data.content_type

    trend = trend_analysis(score, attempts, recent_scores=None)

    pattern = detect_error_pattern(
        expected=data.text,
        spoken=data.spoken,
        content_type=content_type
    )

    feedback_msgs = []

    # -------------------------
    # Verdict (UNCHANGED)
    # -------------------------

    if score >= 90:
        verdict = "excellent"
        feedback_msgs.append("Clear and confident — beautifully spoken 🌟")

    elif score >= 75:
        verdict = "good"
        feedback_msgs.append("You're very close — small adjustments will make it perfect 🔥")

    elif score >= 55:
        verdict = "improving"
        feedback_msgs.append("You’re building fluency. Keep practicing slowly 💪")

    else:
        verdict = "needs_practice"
        feedback_msgs.append("Take your time. Break it into parts and try again 🧠")

    # -------------------------
    # 🔥 AI REASONING (CONTROLLED)
    # -------------------------

    if pattern and pattern.get("code") != "normal":

        try:
            rag_explanation = generate_reasoning(
                expected=data.text,
                spoken=data.spoken,
                pattern=pattern
            )

            # 🔥 CLEAN + FILTER
            rag_explanation = clean_response(rag_explanation)

            if is_bad_response(rag_explanation):
                raise Exception("Bad AI output")

            feedback_msgs.append(rag_explanation)

        except Exception:
            # 🔥 SAFE FALLBACK (CRITICAL FOR PROD)
            feedback_msgs.append(
                "Some sounds are different.\nTry saying it slowly and clearly."
            )

    # -------------------------
    # 🔥 TREND (LOW PRIORITY)
    # -------------------------

    if trend:
        feedback_msgs.append(clean_response(trend["message"]))
        feedback_msgs.append(clean_response(trend["tip"]))

    # -------------------------
    # 🔥 FINAL NORMALIZATION
    # -------------------------

    feedback_msgs = list(dict.fromkeys(feedback_msgs))  # remove duplicates

    # -------------------------
    # Confidence Tip
    # -------------------------

    confidence_tip = (
        "Progress builds with repetition. Speak slowly. Stay consistent 💙"
    )

    return FeedbackOut(
        verdict=verdict,
        score=round(score, 2),
        feedback=feedback_msgs,
        confidence_tip=confidence_tip
    )