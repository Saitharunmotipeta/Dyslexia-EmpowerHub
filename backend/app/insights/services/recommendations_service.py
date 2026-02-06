# app/insights/services/recommendations_service.py

from app.insights.schemas import FeedbackIn, RecommendationOut


def recommend_next_step(data: FeedbackIn) -> RecommendationOut:
    score = data.similarity
    attempts = data.attempts
    pace = data.pace or "medium"

    print("🔍 Recommending next step for word=", data.word, "and spoken=", data.spoken)
    metrics = {
        "score": score,
        "attempts": attempts,
        "pace": pace,
        "word": data.word,
        "spoken": data.spoken
    }

    # =========================
    #  🎯 CASE 1 — Strong mastery
    # =========================
    if score >= 85:
        rec = RecommendationOut(
            recommendation="advance_level",
            headline="Great job! You're ready for the next level 🎯",
            explanation="Your accuracy and consistency show strong mastery.",
            confidence=0.92,
            next_steps=[
                "Continue to the next level",
                "Use the word in daily conversation",
                "Return later to refresh"
            ],
            metrics_used=metrics
        )

        _log_metrics_and_result("advance_level", metrics, rec)
        return rec

    # =========================
    # ✨ CASE 2 — Good but not perfect
    # =========================
    if score >= 70:
        rec = RecommendationOut(
            recommendation="repeat_with_slow_pace",
            headline="Almost there — let's polish pronunciation ✨",
            explanation="Repeating slowly helps strengthen clarity.",
            confidence=0.82,
            next_steps=[
                "Play TTS in slow mode",
                "Repeat syllable-by-syllable",
                "Practice 2–3 times"
            ],
            metrics_used=metrics
        )

        _log_metrics_and_result("repeat_with_slow_pace", metrics, rec)
        return rec

    # =========================
    # 🧩 CASE 3 — Many attempts
    # =========================
    if attempts >= 4:
        rec = RecommendationOut(
            recommendation="breakdown_training",
            headline="Let’s simplify this word step-by-step 🧩",
            explanation="Breaking the word into smaller parts supports recall.",
            confidence=0.88,
            next_steps=[
                "Practice the first syllable",
                "Add syllables gradually",
                "Try recording again after each part"
            ],
            metrics_used=metrics
        )

        _log_metrics_and_result("breakdown_training", metrics, rec)
        return rec

    # =========================
    # 🔁 DEFAULT — Guided retry
    # =========================
    rec = RecommendationOut(
        recommendation="guided_retry",
        headline="Let’s try that again — you’re learning 💪",
        explanation="Repeating helps lock in pronunciation.",
        confidence=0.76,
        next_steps=[
            "Replay the audio",
            "Repeat calmly",
            "Record again when ready"
        ],
        metrics_used=metrics
    )

    _log_metrics_and_result("guided_retry", metrics, rec)
    return rec



def _log_metrics_and_result(decision: str, metrics: dict, rec: RecommendationOut):
    """
    Pretty-print both the decision metrics AND the recommendation result
    so debugging feels like storytelling 📊📖
    """

    print("\n=============== 🤖 RECOMMENDATION ENGINE ===============")
    print(f"📌 Decision     : {decision}")
    print(f"📝 Word         : {metrics.get('word')}")
    print(f"🗣️ Spoken       : {metrics.get('spoken')}")
    print(f"🎯 Score        : {metrics.get('score')}")
    print(f"📊 Attempts     : {metrics.get('attempts')}")
    print(f"⏩ Pace         : {metrics.get('pace')}")
    print("---------------------------------------------------------")
    print("📤 Generated Feedback:")
    print(f"   🧭 Recommendation : {rec.recommendation}")
    print(f"   🏷  Headline       : {rec.headline}")
    print(f"   📖 Explanation    : {rec.explanation}")
    print(f"   🔒 Confidence     : {rec.confidence}")
    print(f"   📌 Next Steps:")
    for step in rec.next_steps:
        print(f"      • {step}")
    print("=========================================================")
