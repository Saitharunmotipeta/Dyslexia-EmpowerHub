# app/feedback/routes/feedback_routes.py

from app.feedback.schemas import FeedbackIn
from app.feedback.services.trends import trend_analysis
from app.feedback.services.pattern_service import detect_error_pattern
from app.feedback.services.feedback_service import generate_feedback


def analyze_trend_handler(data: FeedbackIn):
    return {
        "trend": trend_analysis(data.similarity, data.attempts)
    }


def analyze_pattern_handler(data: FeedbackIn):
    return {
        "pattern": detect_error_pattern(data.word, data.spoken)
    }


def generate_feedback_handler(data: FeedbackIn):
    return generate_feedback(data)
