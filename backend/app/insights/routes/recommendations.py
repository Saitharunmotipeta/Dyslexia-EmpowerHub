from fastapi import Depends
from app.auth.dependencies import get_current_user_id
from app.insights.schemas import FeedbackIn, RecommendationOut
from app.insights.services.recommendations_service import recommend_next_step

def recommendation_endpoint(data: FeedbackIn, user_id: int = Depends(get_current_user_id)) -> RecommendationOut:
    """
    Accepts feedback metrics
    Returns next-step recommendation
    """
    return recommend_next_step(data)
