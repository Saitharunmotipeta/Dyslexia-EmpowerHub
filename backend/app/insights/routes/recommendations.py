# app/feedback/routes/recommendations.py

from app.insights.schemas import FeedbackIn, RecommendationOut
from app.insights.services.recommendations_service import recommend_next_step


def recommendation_endpoint(
    data: FeedbackIn,
    user_id: int
) -> RecommendationOut:
    return recommend_next_step(data)
