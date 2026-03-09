# app/insights/services/recommendations_service.py

from app.insights.schemas import FeedbackIn, RecommendationOut


def recommend_next_step(data: FeedbackIn) -> RecommendationOut:
    score = data.score
    attempts = data.attempts
    pace = data.pace or 0.9
    content_type = data.content_type

    metrics = {
        "score": score,
        "attempts": attempts,
        "pace": pace,
        "text": data.text,
        "spoken": data.spoken,
        "content_type": content_type
    }

    if score >= 85:
        rec = RecommendationOut(
            recommendation="advance_level",
            headline="Great progress — you're ready to move forward 🎯",
            explanation="Your pronunciation shows strong control and clarity.",
            confidence=0.92,
            next_steps=[
                "Try a harder word or sentence",
                "Use it in conversation",
                "Return later to reinforce it"
            ],
            metrics_used=metrics
        )

        return rec

    if score >= 70:
        rec = RecommendationOut(
            recommendation="slow_repeat",
            headline="Almost there — slow it down slightly ✨",
            explanation="Repeating slowly improves sound clarity.",
            confidence=0.82,
            next_steps=[
                "Replay TTS in slow mode",
                "Repeat syllable-by-syllable",
                "Record again calmly"
            ],
            metrics_used=metrics
        )

        return rec

    if content_type in ["phrase", "sentence"] and score < 60:
        rec = RecommendationOut(
            recommendation="segment_practice",
            headline="Break the sentence into smaller parts 🧩",
            explanation="Practicing one word at a time helps fluency.",
            confidence=0.88,
            next_steps=[
                "Say one word at a time",
                "Combine two words slowly",
                "Speak full sentence again"
            ],
            metrics_used=metrics
        )

        return rec

    if attempts >= 4:
        rec = RecommendationOut(
            recommendation="guided_break",
            headline="Let’s reset and try calmly 💙",
            explanation="Fatigue can affect pronunciation accuracy.",
            confidence=0.80,
            next_steps=[
                "Take a short pause",
                "Listen carefully to TTS",
                "Try once more with focus"
            ],
            metrics_used=metrics
        )

        return rec

    rec = RecommendationOut(
        recommendation="guided_retry",
        headline="Keep practicing — you're improving 💪",
        explanation="Repetition strengthens pronunciation memory.",
        confidence=0.76,
        next_steps=[
            "Replay the audio",
            "Repeat slowly",
            "Record again when ready"
        ],
        metrics_used=metrics
    )

    return rec
