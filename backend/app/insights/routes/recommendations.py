from app.insights.schemas import FeedbackIn, RecommendationOut
from app.insights.services.recommendations_service import recommend_next_step


def recommendation_endpoint(data: FeedbackIn) -> RecommendationOut:
    """
    Accepts feedback metrics
    Returns next-step recommendation
    """
    return recommend_next_step(data)
