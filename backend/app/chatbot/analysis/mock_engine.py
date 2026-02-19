from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.mock.models.attempt import MockAttempt


def run(user_id: int, db: Session) -> dict | None:

    attempts = (
        db.query(MockAttempt)
        .filter(MockAttempt.user_id == user_id)
        .order_by(desc(MockAttempt.completed_at))
        .limit(5)
        .all()
    )

    if not attempts:
        return None

    scores = [
        a.total_score
        for a in attempts
        if a.total_score is not None
    ]

    avg_score = round(sum(scores) / len(scores), 2) if scores else None

    return {
        "recent_mock_attempts": len(attempts),
        "average_mock_score": avg_score,
        "latest_mock_score": scores[0] if scores else None,
    }
