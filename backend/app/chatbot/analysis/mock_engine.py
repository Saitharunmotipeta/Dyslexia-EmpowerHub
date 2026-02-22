from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.mock.models.attempt import MockAttempt


PASS_THRESHOLD = 60  # You said you use 80


def run(user_id: int, db: Session, mode: str = "latest") -> dict | None:

    attempts = (
        db.query(MockAttempt)
        .filter(
            MockAttempt.user_id == user_id,
            MockAttempt.total_score != None
        )
        .order_by(desc(MockAttempt.completed_at))
        .limit(5)
        .all()
    )

    if not attempts:
        return None

    # Convert to percentages (assuming total_score already percent)
    scores = [round(a.total_score, 2) for a in attempts]

    # -----------------------------
    # Mode 1: Latest Mock Only
    # -----------------------------
    if mode == "latest":

        latest = attempts[0]
        score = scores[0]

        return {
            "mock_id": latest.public_attempt_id,
            "level_id": latest.level_id,
            "completed_at": latest.completed_at,
            "score_percent": score,
            "below_threshold": score < PASS_THRESHOLD,
        }

    # -----------------------------
    # Mode 2: Trend / Aggregate
    # -----------------------------
    avg_score = round(sum(scores) / len(scores), 2)

    improvement = None
    if len(scores) >= 2:
        improvement = scores[0] - scores[-1]

    return {
        "recent_mock_count": len(attempts),
        "average_mock_score": avg_score,
        "latest_mock_score": scores[0],
        "trend_difference": improvement,
    }