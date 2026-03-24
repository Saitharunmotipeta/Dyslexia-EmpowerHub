from app.insights.schemas import FeedbackIn, RecommendationOut
from app.insights.services.word_generator import generate_similar_words


def extract_score(value):
    if isinstance(value, dict):
        return value.get("percentage", 0)
    return value


def recommend_next_step(
    data: FeedbackIn,
    weakness_heatmap: dict | None = None,
    pattern: dict | None = None,
    mistakes: list[str] | None = None   # 🔥 NEW
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

    mistakes = mistakes or []

    # -------------------------
    # 🔥 STEP 1: USE MISTAKES FIRST (CORE FIX)
    # -------------------------
    if mistakes:
        return RecommendationOut(
            recommendation="practice_target_words",
            headline="Practice these words 🔁",
            explanation="These words were mispronounced.",
            confidence=0.95,
            next_steps=mistakes[:3],
            metrics_used=metrics
        )

    # -------------------------
    # 🔥 STEP 2: FALLBACK WORD GENERATION
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
            explanation="These target your mistake indirectly.",
            confidence=0.85,
            next_steps=words,
            metrics_used=metrics
        )

    # -------------------------
    # 🔥 STEP 3: WEAKNESS EXTRACTION
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
    # 🔥 STEP 4: HIGH SCORE
    # -------------------------
    if score >= 85:
        return RecommendationOut(
            recommendation="advance_level",
            headline="Great progress — move ahead 🚀",
            explanation="Your pronunciation is clear and confident.",
            confidence=0.9,
            next_steps=[
                "Try saying the full sentence smoothly",
                "Focus on natural rhythm",
                "Record yourself and compare"
            ],
            metrics_used=metrics
        )

    # -------------------------
    # 🔥 STEP 5: FATIGUE
    # -------------------------
    if attempts >= 4:
        return RecommendationOut(
            recommendation="guided_break",
            headline="Take a short reset 💙",
            explanation="Break helps improve clarity.",
            confidence=0.82,
            next_steps=[
                "Say it slowly",
                "Focus on each word",
                "Try again calmly"
            ],
            metrics_used=metrics
        )

    # -------------------------
    # 🔥 STEP 6: MID RANGE
    # -------------------------
    if score >= 60:
        return RecommendationOut(
            recommendation="slow_repeat",
            headline="Almost there — refine it ✨",
            explanation="Small adjustments will help.",
            confidence=0.82,
            next_steps=[
                "Practice the difficult words",
                "Say the full sentence slowly",
                "Try again calmly"
            ],
            metrics_used=metrics
        )

    # -------------------------
    # 🔥 STEP 7: FALLBACK
    # -------------------------
    return RecommendationOut(
        recommendation="guided_retry",
        headline="Keep going 💪",
        explanation="Practice step by step.",
        confidence=0.75,
        next_steps=[
            "Break sentence into words",
            "Say each word clearly",
            "Try again slowly"
        ],
        metrics_used=metrics
    )