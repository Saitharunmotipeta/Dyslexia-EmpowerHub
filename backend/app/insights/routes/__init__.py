# app/feedback/routes/__init__.py

from fastapi import APIRouter, Depends
from app.auth.dependencies import get_current_user_id
from app.insights.schemas import FeedbackIn
from app.insights.routes.feedback import (
    analyze_trend_handler,
    analyze_pattern_handler,
    generate_feedback_handler
)
from app.insights.routes.recommendations import recommendation_endpoint
from app.insights.routes.aggregate import aggregate_feedback_handler


router = APIRouter(prefix="/feedback", tags=["Insights"])


@router.post("/trend")
def analyze_trend(data: FeedbackIn, user_id: int = Depends(get_current_user_id)):
    """
    Analyzes user's feedback trend.

    Args:
        data (FeedbackIn): Contains user's feedback metrics.
        user_id (int): User's ID.

    Returns:
        dict: Containing trend analysis result.
    """
    return analyze_trend_handler(data, user_id)


@router.post("/pattern")
def analyze_pattern(data: FeedbackIn, user_id: int = Depends(get_current_user_id)):
    """
    Analyzes user's feedback pattern.

    Args:
        data (FeedbackIn): Contains user's feedback metrics.
        user_id (int): User's ID.

    Returns:
        dict: Containing pattern analysis result.
    """
    return analyze_pattern_handler(data,user_id)


@router.post("/generate")
def generate_feedback(data: FeedbackIn, user_id: int = Depends(get_current_user_id)):
    return generate_feedback_handler(data,user_id)

@router.post("/recommendation")
def recommendation(data: FeedbackIn, user_id: int = Depends(get_current_user_id)):
    return recommendation_endpoint(data,user_id)

@router.post("/aggregate")
def aggregate_feedback(
    data: FeedbackIn,
    user_id: int = Depends(get_current_user_id),
):
    """
    Aggregates all feedback metrics into one response.

    Args:
        data (FeedbackIn): Contains user's feedback metrics.
        user_id (int): User's ID.

    Returns:
        dict: Containing aggregated feedback result.
    """
    return aggregate_feedback_handler(data, user_id)