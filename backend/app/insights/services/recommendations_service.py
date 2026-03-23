from app.insights.schemas import FeedbackIn, RecommendationOut
from app.insights.services.word_generator import generate_similar_words


def extract_score(value):
    if isinstance(value, dict):
        return value.get("percentage", 0)
    return value


def recommend_next_step(
    data: FeedbackIn,
    weakness_heatmap: dict | None = None,
    pattern: dict | None = None
) -> RecommendationOut:

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

    # -------------------------
    # 🔥 STEP 1: ALWAYS TRY WORD GENERATION FIRST
    # -------------------------

    words = generate_similar_words(
        expected=data.text,
        spoken=data.spoken,
        pattern=pattern
    )

    if words and isinstance(words, list) and len(words) > 0:
        return RecommendationOut(
            recommendation="practice_generated_words",
            headline="Practice these sounds 🔁",
            explanation="These target your mistake directly.",
            confidence=0.95,
            next_steps=words,
            metrics_used=metrics
        )

    # -------------------------
    # 🔥 STEP 2: WEAKNESS EXTRACTION
    # -------------------------
    focus = "general"
    focus_score = 0

    if weakness_heatmap:
        valid_keys = [
            k for k, v in weakness_heatmap.items()
            if isinstance(v, (int, float)) or (isinstance(v, dict) and "percentage" in v)
        ]

        if valid_keys:
            focus = max(
                valid_keys,
                key=lambda k: extract_score(weakness_heatmap[k])
            )
            focus_score = extract_score(weakness_heatmap[focus])

    # -------------------------
    # 🔥 STEP 3: HIGH SCORE
    # -------------------------
    if score >= 85:
        return RecommendationOut(
            recommendation="advance_level",
            headline="Great progress — move ahead 🚀",
            explanation="Your pronunciation is clear and confident.",
            confidence=0.9,
            next_steps=["Try a longer sentence", "Focus on natural rhythm", "Record yourself and compare"],
            metrics_used=metrics
        )

    # -------------------------
    # 🔥 STEP 4: FATIGUE
    # -------------------------
    if attempts >= 4:
        return RecommendationOut(
            recommendation="guided_break",
            headline="Take a short reset 💙",
            explanation="Break helps improve clarity.",
            confidence=0.82,
            next_steps=[
                    "Say it slowly",
                    "Focus on each sound",
                    "Try again calmly"
                ],
            metrics_used=metrics
        )

    # -------------------------
    # 🔥 STEP 5: MID RANGE
    # -------------------------
    if score >= 60:
        return RecommendationOut(
            recommendation="slow_repeat",
            headline="Almost there — refine it ✨",
            explanation="Small adjustments will help.",
            confidence=0.82,
            next_steps=["Focus on the {} sound.".format(focus) if focus != "general" else "Try saying it slowly and clearly. Focus on each sound.", "Try again calmly", "Record yourself and compare"],
            metrics_used=metrics
        )
    

    # -------------------------
    # 🔥 STEP 6: FALLBACK
    # -------------------------
    return RecommendationOut(
        recommendation="guided_retry",
        headline="Keep going 💪",
        explanation="Practice step by step.",
        confidence=0.75,
        next_steps=words if words else ["Try saying it slowly and clearly. Focus on each sound.", "Try again calmly", "Record yourself and compare"],
        metrics_used=metrics
    )