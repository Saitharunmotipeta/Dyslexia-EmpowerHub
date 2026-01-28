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

router = APIRouter(prefix="/feedback", tags=["Feedback"])


@router.post("/trend")
def analyze_trend(data: FeedbackIn, user_id: int = Depends(get_current_user_id)):
    return analyze_trend_handler(data, user_id)


@router.post("/pattern")
def analyze_pattern(data: FeedbackIn, user_id: int = Depends(get_current_user_id)):
    return analyze_pattern_handler(data,user_id)


@router.post("/generate")
def generate_feedback(data: FeedbackIn, user_id: int = Depends(get_current_user_id)):
    return generate_feedback_handler(data,user_id)

@router.post("/recommendation")
def recommendation(data: FeedbackIn, user_id: int = Depends(get_current_user_id)):
    return recommendation_endpoint(data,user_id)