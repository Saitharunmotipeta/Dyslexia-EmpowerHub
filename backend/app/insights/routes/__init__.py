# app/feedback/routes/__init__.py

from fastapi import APIRouter
from app.insights.schemas import FeedbackIn
from app.insights.routes.feedback import (
    analyze_trend_handler,
    analyze_pattern_handler,
    generate_feedback_handler
)
from app.insights.routes.recommendations import recommendation_endpoint

router = APIRouter(prefix="/feedback", tags=["Feedback"])


@router.post("/trend")
def analyze_trend(data: FeedbackIn):
    return analyze_trend_handler(data)


@router.post("/pattern")
def analyze_pattern(data: FeedbackIn):
    return analyze_pattern_handler(data)


@router.post("/generate")
def generate_feedback(data: FeedbackIn):
    return generate_feedback_handler(data)

@router.post("/recommendation")
def recommendation(data: FeedbackIn):
    return recommendation_endpoint(data)