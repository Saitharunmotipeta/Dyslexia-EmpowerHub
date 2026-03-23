# app/feedback/routes/aggregate.py

from sqlalchemy.orm import Session

from app.insights.schemas import FeedbackIn

from app.insights.routes.feedback import (
    analyze_trend_handler,
    analyze_pattern_handler,
    generate_feedback_handler,
)
from app.insights.routes.recommendations import recommendation_endpoint


def aggregate_feedback_handler(
    data: FeedbackIn,
    db: Session,
    user_id: int,
):
    """
    Unified feedback engine.
    Runs trend + pattern + feedback + recommendation.
    """

    trend_result = analyze_trend_handler(data, user_id)
    pattern = analyze_pattern_handler(data, user_id)

    feedback_result = generate_feedback_handler(data, db, user_id)

    recommendation_result = recommendation_endpoint(
        data=data,
        db=db,
        user_id=user_id,
        pattern=pattern
    )

    return {
        "trend": trend_result.get("trend"),
        "pattern": pattern,
        "feedback": feedback_result,
        "recommendation": recommendation_result,
    }