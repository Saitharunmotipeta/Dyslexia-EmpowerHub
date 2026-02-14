# app/feedback/routes/aggregate.py

from app.insights.schemas import FeedbackIn

from app.insights.routes.feedback import (
    analyze_trend_handler,
    analyze_pattern_handler,
    generate_feedback_handler,
)
from app.insights.routes.recommendations import recommendation_endpoint


def aggregate_feedback_handler(
    data: FeedbackIn,
    user_id: int,
):
    """
    Unified feedback engine.
    Runs trend + pattern + feedback + recommendation.
    """

    trend_result = analyze_trend_handler(data, user_id)
    pattern_result = analyze_pattern_handler(data, user_id)
    feedback_result = generate_feedback_handler(data, user_id)
    recommendation_result = recommendation_endpoint(data, user_id)

    return {
        "trend": trend_result.get("trend"),
        "pattern": pattern_result.get("pattern"),
        "feedback": feedback_result,
        "recommendation": recommendation_result,
    }
