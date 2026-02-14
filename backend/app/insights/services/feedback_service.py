# app/feedback/services/feedback_service.py

from app.insights.schemas import FeedbackIn, FeedbackOut
from app.insights.services.trends import trend_analysis
from app.insights.services.pattern_service import detect_error_pattern


def generate_feedback(data: FeedbackIn) -> FeedbackOut:

    score = data.score
    attempts = data.attempts
    content_type = data.content_type

    print("🔍 Generating feedback for text=", data.text, "spoken=", data.spoken)

    # ----------------------------
    # 📈 TREND ANALYSIS
    # ----------------------------
    trend = trend_analysis(score, attempts, recent_scores=None)

    # ----------------------------
    # 🔍 PATTERN DETECTION
    # ----------------------------
    pattern = detect_error_pattern(
        expected=data.text,
        spoken=data.spoken,
        content_type=content_type
    )

    feedback_msgs = []

    # ----------------------------
    # 🎯 SCORE-BASED VERDICT
    # ----------------------------
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

    # ----------------------------
    # 🔍 PATTERN-DRIVEN COACHING
    # ----------------------------
    if pattern and pattern.get("code") != "normal":
        feedback_msgs.append(pattern["message"])
        feedback_msgs.append(pattern["tip"])

    # ----------------------------
    # 📈 TREND-BASED COACHING
    # ----------------------------
    if trend:
        feedback_msgs.append(trend["message"])
        feedback_msgs.append(trend["tip"])

    # ----------------------------
    # 🧠 CONFIDENCE TIP
    # ----------------------------
    confidence_tip = (
        "Progress builds with repetition. Speak slowly. Stay consistent 💙"
    )

    print("\n========== 🧠 GENERATED FEEDBACK DEBUG ==========")
    print(f"🎯 Verdict         : {verdict}")
    print(f"📊 Score           : {round(score, 2)}")
    print("=================================================\n")

    return FeedbackOut(
        verdict=verdict,
        score=round(score, 2),
        feedback=list(dict.fromkeys(feedback_msgs)),
        confidence_tip=confidence_tip
    )
