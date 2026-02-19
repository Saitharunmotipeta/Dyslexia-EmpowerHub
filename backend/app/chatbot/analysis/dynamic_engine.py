# app/chatbot/analysis/dynamic_engine.py

from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.dynamic.models.dynamic_attempt import DynamicAttempt  # adjust path if needed


def run(user_id: int, db: Session) -> dict | None:
    """
    Analyze recent dynamic attempts for a user.
    Returns structured summary only.
    """

    attempts = (
        db.query(DynamicAttempt)
        .filter(DynamicAttempt.user_id == user_id)
        .order_by(desc(DynamicAttempt.created_at))
        .limit(5)
        .all()
    )

    if not attempts:
        return None

    scores = [a.score for a in attempts if a.score is not None]

    avg_score = None
    latest_score = None

    if scores:
        avg_score = round(sum(scores) / len(scores), 2)
        latest_score = scores[0]

    return {
        "recent_dynamic_attempts": len(attempts),
        "latest_dynamic_score": latest_score,
        "average_dynamic_score": avg_score,
    }
