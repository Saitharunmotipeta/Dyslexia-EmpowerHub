# app/feedback/services/feedback_service.py

from app.insights.schemas import FeedbackIn, FeedbackOut
from app.insights.services.trends import trend_analysis
from app.insights.services.pattern_service import detect_error_pattern


def generate_feedback(data: FeedbackIn) -> FeedbackOut:

    score = data.similarity
    attempts = data.attempts

    print("🔍 Generating feedback for word=", data.word, "and spoken=", data.spoken)
    trend = trend_analysis(score, attempts, recent_scores=None)
    pattern = detect_error_pattern(data.word, data.spoken)

    feedback_msgs = []

    # ----------------------------
    # 🎯 SCORE-BASED VERDICT
    # ----------------------------
    if score >= 90:
        verdict = "excellent"
        feedback_msgs.append("Crystal-clear pronunciation — that was chef-kiss perfect 💫")

    elif score >= 75:
        verdict = "good"
        feedback_msgs.append("So close — just polish the edges 🔥")

    elif score >= 55:
        verdict = "improving"
        feedback_msgs.append("You're building the muscle memory. Keep stacking reps 💪")

    else:
        verdict = "needs_practice"
        feedback_msgs.append("No worries — slow it down and give it another try 🧠")


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
    # 🧠 CONFIDENCE TIP — ALWAYS KIND
    # ----------------------------
    confidence_tip = "Progress isn't linear — but you're trending upward. Stay in the game 💙"

    print("\n========== 🧠 GENERATED FEEDBACK DEBUG ==========")
    print(f"🎯 Verdict         : {verdict}")
    print(f"📊 Score           : {round(score, 2)}")
    print(f"💬 Feedback Lines  :")
    for msg in feedback_msgs:
        print(f"   • {msg}")
    print(f"✨ Confidence Tip  : {confidence_tip}")
    print("=================================================\n")



    return FeedbackOut(
        verdict=verdict,
        score=round(score, 2),
        feedback=list(dict.fromkeys(feedback_msgs)),  # remove dupes but keep order
        confidence_tip=confidence_tip
    )
