# app/feedback/routes/__init__.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from difflib import SequenceMatcher  # 🔥 NEW

from app.auth.dependencies import get_current_user_id
from app.database.connection import get_db

from app.insights.schemas import FeedbackIn

from app.insights.routes.feedback import (
    analyze_trend_handler,
    analyze_pattern_handler,
    generate_feedback_handler
)

from app.insights.routes.recommendations import recommendation_endpoint
from app.insights.routes.aggregate import aggregate_feedback_handler
from app.insights.routes.aggregate import align_words  # 🔥 NEW


router = APIRouter(prefix="/feedback", tags=["Insights"])


@router.post("/trend")
def analyze_trend(
    data: FeedbackIn,
    user_id: int = Depends(get_current_user_id)
):
    return analyze_trend_handler(data, user_id)


@router.post("/pattern")
def analyze_pattern(
    data: FeedbackIn,
    user_id: int = Depends(get_current_user_id)
):
    return analyze_pattern_handler(data, user_id)


@router.post("/generate")
def generate_feedback(
    data: FeedbackIn,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    return generate_feedback_handler(data, db, user_id)


# 🔥 UPDATED
@router.post("/recommendation")
def recommendation(
    data: FeedbackIn,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    alignment = align_words(data.text, data.spoken)  # 🔥 NEW

    pattern_result = analyze_pattern_handler(
        data,
        user_id,
        alignment=alignment   # 🔥 NEW
    )

    return recommendation_endpoint(
        data,
        db,
        user_id,
        pattern_result.get("pattern"),
        alignment=alignment   # 🔥 NEW
    )


@router.post("/aggregate")
def aggregate_feedback(
    data: FeedbackIn,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    return aggregate_feedback_handler(data, db, user_id)