from app.insights.schemas import FeedbackIn, RecommendationOut


def recommend_next_step(
    data: FeedbackIn,
    weakness_heatmap: dict | None = None,
    confidence_index: dict | None = None
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
    # Weakness signals
    # -------------------------

    vowel_issue = weakness_heatmap and weakness_heatmap.get("vowel", 0) > 25
    start_issue = weakness_heatmap and weakness_heatmap.get("initial_sound", 0) > 25
    end_issue = weakness_heatmap and weakness_heatmap.get("final_sound", 0) > 25

    confidence_level = None
    if confidence_index:
        confidence_level = confidence_index.get("confidence_level")

    # -------------------------
    # Excellent performance
    # -------------------------

    if score >= 85:

        headline = "Great progress — you're ready to move forward 🎯"

        if confidence_level == "advanced":
            headline = "Excellent pronunciation — keep building fluency 🌟"

        return RecommendationOut(
            recommendation="advance_level",
            headline=headline,
            explanation="Your pronunciation shows strong clarity and confidence.",
            confidence=0.92,
            next_steps=[
                "Try a harder word or sentence",
                "Use it in conversation",
                "Return later to reinforce it"
            ],
            metrics_used=metrics
        )

    # -------------------------
    # Small improvements needed
    # -------------------------

    if score >= 70:

        tips = [
            "Replay TTS in slow mode",
            "Repeat syllable-by-syllable",
            "Record again calmly"
        ]

        if vowel_issue:
            tips.insert(0, "Focus on vowel sounds — stretch them slightly")

        return RecommendationOut(
            recommendation="slow_repeat",
            headline="Almost there — slow it down slightly ✨",
            explanation="Repeating slowly improves sound clarity.",
            confidence=0.82,
            next_steps=tips,
            metrics_used=metrics
        )

    # -------------------------
    # Sentence segmentation
    # -------------------------

    if content_type in ["phrase", "sentence"] and score < 60:

        return RecommendationOut(
            recommendation="segment_practice",
            headline="Break the sentence into smaller parts 🧩",
            explanation="Practicing one word at a time improves fluency.",
            confidence=0.88,
            next_steps=[
                "Say one word at a time",
                "Combine two words slowly",
                "Speak the full sentence again"
            ],
            metrics_used=metrics
        )

    # -------------------------
    # Fatigue detection
    # -------------------------

    if attempts >= 4:

        return RecommendationOut(
            recommendation="guided_break",
            headline="Let’s reset and try calmly 💙",
            explanation="Taking a short break helps your speech reset.",
            confidence=0.80,
            next_steps=[
                "Take a short pause",
                "Listen carefully to the example audio",
                "Try again when relaxed"
            ],
            metrics_used=metrics
        )

    # -------------------------
    # Weakness-based hints
    # -------------------------

    if vowel_issue:

        return RecommendationOut(
            recommendation="vowel_focus",
            headline="Focus on vowel clarity 🔊",
            explanation="Your vowel sounds need a bit more precision.",
            confidence=0.75,
            next_steps=[
                "Stretch the vowel sound slowly",
                "Repeat the word three times",
                "Compare with the audio example"
            ],
            metrics_used=metrics
        )

    if start_issue:

        return RecommendationOut(
            recommendation="initial_sound_focus",
            headline="Start the word clearly 🎙️",
            explanation="Beginning sounds help listeners understand the word.",
            confidence=0.74,
            next_steps=[
                "Emphasize the first sound",
                "Say the first syllable slowly",
                "Repeat the full word again"
            ],
            metrics_used=metrics
        )

    if end_issue:

        return RecommendationOut(
            recommendation="final_sound_focus",
            headline="Finish the word fully ✨",
            explanation="Completing the ending sound improves clarity.",
            confidence=0.74,
            next_steps=[
                "Slow the final syllable",
                "Pause slightly before finishing",
                "Repeat again"
            ],
            metrics_used=metrics
        )

    # -------------------------
    # Default guidance
    # -------------------------

    return RecommendationOut(
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