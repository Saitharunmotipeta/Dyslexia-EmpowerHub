# app/feedback/routes/feedback_routes.py
from fastapi import Depends
from app.auth.dependencies import get_current_user_id
from app.insights.schemas import FeedbackIn
from app.insights.services.trends import trend_analysis
from app.insights.services.pattern_service import detect_error_pattern
from app.insights.services.feedback_service import generate_feedback

def analyze_trend_handler(data: FeedbackIn, user_id: int):
    return {
        "trend": trend_analysis(data.similarity, data.attempts, recent_scores=None,)
    }

def analyze_pattern_handler(data: FeedbackIn, user_id: int ):
    return {
        "pattern": detect_error_pattern(data.word, data.spoken,)
    }


def generate_feedback_handler(data: FeedbackIn, user_id: int ):
    return generate_feedback(data)
