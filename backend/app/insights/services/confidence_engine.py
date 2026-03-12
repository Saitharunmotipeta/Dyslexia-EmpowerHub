from statistics import mean, pstdev
from sqlalchemy.orm import Session

from app.mock.models.attempt import MockAttempt


def calculate_confidence_index(db: Session, user_id: int):

    attempts = (
        db.query(MockAttempt)
        .filter(
            MockAttempt.user_id == user_id,
            MockAttempt.status == "completed"
        )
        .order_by(MockAttempt.completed_at)
        .all()
    )

    if not attempts:
        return {
            "confidence_score": 0,
            "confidence_level": "beginner",
            "message": "Start practicing — every word builds confidence 🌱"
        }

    scores = [a.total_score for a in attempts if a.total_score]

    avg_score = mean(scores)

    # -------------------
    # Trend
    # -------------------

    trend = 0
    if len(scores) >= 2:
        trend = scores[-1] - scores[-2]

    # -------------------
    # Consistency
    # -------------------

    stability_bonus = 0

    if len(scores) > 1:
        deviation = pstdev(scores)

        if deviation < 8:
            stability_bonus = 5
        elif deviation > 20:
            stability_bonus = -5

    # -------------------
    # Final confidence
    # -------------------

    confidence = avg_score + (trend * 0.3) + stability_bonus
    confidence = max(0, min(100, round(confidence, 2)))

    # -------------------
    # Level classification
    # -------------------

    if confidence >= 85:
        level = "advanced"
        message = "Your speech sounds confident and consistent 🌟"

    elif confidence >= 65:
        level = "growing"
        message = "Your confidence is steadily improving 💪"

    else:
        level = "developing"
        message = "Keep practicing slowly — confidence grows with repetition 🌱"

    return {
        "confidence_score": confidence,
        "confidence_level": level,
        "mock_average": round(avg_score, 2),
        "trend_change": round(trend, 2),
        "message": message
    }