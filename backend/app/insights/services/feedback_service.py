# app/feedback/services/feedback_service.py

from app.insights.schemas import FeedbackIn, FeedbackOut
from app.insights.services.trends import trend_analysis
from app.insights.services.pattern_service import detect_error_pattern


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

    if pattern and pattern.get("code") != "normal":
        feedback_msgs.append(pattern["message"])
        feedback_msgs.append(pattern["tip"])

    if trend:
        feedback_msgs.append(trend["message"])
        feedback_msgs.append(trend["tip"])

    confidence_tip = (
        "Progress builds with repetition. Speak slowly. Stay consistent 💙"
    )

    return FeedbackOut(
        verdict=verdict,
        score=round(score, 2),
        feedback=list(dict.fromkeys(feedback_msgs)),
        confidence_tip=confidence_tip
    )
