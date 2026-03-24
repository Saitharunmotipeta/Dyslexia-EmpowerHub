# app/feedback/routes/feedback_routes.py

from sqlalchemy.orm import Session
from fastapi import Depends
from app.database.connection import get_db
from app.auth.dependencies import get_current_user_id
from app.insights.schemas import FeedbackIn
from app.insights.services.trends import trend_analysis
from app.insights.services.pattern_service import detect_error_pattern
from app.insights.services.feedback_service import generate_feedback


def analyze_trend_handler(data: FeedbackIn, user_id: int):
    return {
        "trend": trend_analysis(
            score=data.score,
            attempts=data.attempts,
            recent_scores=None,
        )
    }


# 🔥 UPDATED: ADD alignment
def analyze_pattern_handler(data: FeedbackIn, user_id: int, alignment=None):
    return {
        "pattern": detect_error_pattern(
            expected=data.text,
            spoken=data.spoken,
            content_type=data.content_type,
            alignment=alignment,   # 🔥 NEW
        )
    }


# 🔥 UPDATED: ADD alignment
def generate_feedback_handler(
    data: FeedbackIn,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
    alignment=None
):
    return generate_feedback(
        data,
        db,
        user_id,
        alignment=alignment   # 🔥 NEW
    )