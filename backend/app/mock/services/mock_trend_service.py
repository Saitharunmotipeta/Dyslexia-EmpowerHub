from sqlalchemy.orm import Session
from datetime import datetime
from statistics import mean, pstdev

from app.mock.models.attempt import MockAttempt


def analyze_mock_trend(db: Session, user_id: int, level_id: int):

    attempts = (
        db.query(MockAttempt)
        .filter(
            MockAttempt.user_id == user_id,
            MockAttempt.level_id == level_id,
            MockAttempt.status == "completed"
        )
        .order_by(MockAttempt.completed_at.desc())
        .limit(5)
        .all()
    )

    if len(attempts) < 2:
        return None

    scores = [a.total_score or 0 for a in attempts]

    current = scores[0]
    previous = scores[1]

    change = round(current - previous, 2)

    avg_score = round(mean(scores), 2)
    variability = round(pstdev(scores), 2) if len(scores) > 2 else 0

    # -----------------------------
    # TREND DIRECTION
    # -----------------------------
    if change > 5:
        trend = "strong_improvement"
        message = "Your pronunciation is improving clearly 📈"
        tip = "Keep practicing regularly to maintain this growth."

    elif change > 0:
        trend = "slight_improvement"
        message = "Nice progress — you're moving forward."
        tip = "Try practicing slowly to strengthen difficult sounds."

    elif change == 0:
        trend = "stable"
        message = "Your performance is consistent."
        tip = "Focus on specific sounds to push your score higher."

    else:
        trend = "decline"
        message = "This attempt felt slightly harder."
        tip = "Take a short break and try again slowly."

    # -----------------------------
    # CONSISTENCY
    # -----------------------------
    if variability < 5:
        consistency = "very_consistent"
    elif variability < 10:
        consistency = "consistent"
    else:
        consistency = "variable"

    # -----------------------------
    # PRACTICE FREQUENCY
    # -----------------------------
    if attempts[0].completed_at and attempts[1].completed_at:
        days_gap = (
            attempts[0].completed_at - attempts[1].completed_at
        ).days

        if days_gap <= 1:
            practice_pattern = "frequent"
        elif days_gap <= 3:
            practice_pattern = "regular"
        else:
            practice_pattern = "infrequent"
    else:
        practice_pattern = "unknown"

    # -----------------------------
    # CONFIDENCE INDICATOR
    # -----------------------------
    confidence_index = round((current + avg_score) / 2, 2)

    if confidence_index >= 85:
        confidence_level = "very_confident"
    elif confidence_index >= 70:
        confidence_level = "confident"
    elif confidence_index >= 55:
        confidence_level = "developing"
    else:
        confidence_level = "needs_guidance"

    return {
        "trend": trend,
        "previous_score": previous,
        "current_score": current,
        "change": change,
        "average_score": avg_score,
        "consistency": consistency,
        "practice_pattern": practice_pattern,
        "confidence_index": confidence_index,
        "confidence_level": confidence_level,
        "message": message,
        "tip": tip
    }