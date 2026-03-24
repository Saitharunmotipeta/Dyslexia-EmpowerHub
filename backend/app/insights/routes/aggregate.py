# app/feedback/routes/aggregate.py

from sqlalchemy.orm import Session
from difflib import SequenceMatcher

from app.insights.schemas import FeedbackIn

from app.insights.routes.feedback import (
    analyze_trend_handler,
    analyze_pattern_handler,
    generate_feedback_handler,
)
from app.insights.routes.recommendations import recommendation_endpoint


# -------------------------
# 🔥 NEW: ALIGNMENT ENGINE
# -------------------------
def align_words(expected: str, spoken: str):
    exp = expected.lower().split()
    spk = spoken.lower().split()

    matcher = SequenceMatcher(None, exp, spk)
    result = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            for i in range(i2 - i1):
                result.append({
                    "type": "correct",
                    "expected": exp[i1 + i],
                    "spoken": spk[j1 + i]
                })

        elif tag == "replace":
            for i in range(max(i2 - i1, j2 - j1)):
                result.append({
                    "type": "substitution",
                    "expected": exp[i1 + i] if i1 + i < i2 else None,
                    "spoken": spk[j1 + i] if j1 + i < j2 else None
                })

        elif tag == "delete":
            for i in range(i1, i2):
                result.append({
                    "type": "missing",
                    "expected": exp[i]
                })

        elif tag == "insert":
            for j in range(j1, j2):
                result.append({
                    "type": "extra",
                    "spoken": spk[j]
                })

    return result


def aggregate_feedback_handler(
    data: FeedbackIn,
    db: Session,
    user_id: int,
):
    """
    Unified feedback engine.
    Runs trend + pattern + feedback + recommendation.
    """

    # -------------------------
    # 🔥 NEW: COMPUTE ALIGNMENT ONCE
    # -------------------------
    alignment = align_words(data.text, data.spoken)

    # -------------------------
    # EXISTING FLOW (ENHANCED)
    # -------------------------
    trend_result = analyze_trend_handler(data, user_id)

    pattern = analyze_pattern_handler(
        data,
        user_id,
        alignment=alignment   # 🔥 NEW
    )

    feedback_result = generate_feedback_handler(
        data,
        db,
        user_id,
        alignment=alignment   # 🔥 NEW
    )

    recommendation_result = recommendation_endpoint(
        data=data,
        db=db,
        user_id=user_id,
        pattern=pattern,
        alignment=alignment   # 🔥 NEW
    )

    return {
        "trend": trend_result.get("trend"),
        "pattern": pattern,
        "feedback": feedback_result,
        "recommendation": recommendation_result,
    }