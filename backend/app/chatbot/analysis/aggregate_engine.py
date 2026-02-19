# app/chatbot/analysis/aggregate_engine.py

from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.mock.models.attempt import MockAttempt
from app.dynamic.models.dynamic_attempt import DynamicAttempt
from app.learning.models.level_word import LevelWord


def run(user_id: int, db: Session) -> dict | None:

    # Recent mock attempts
    recent_mocks = (
        db.query(MockAttempt)
        .filter(MockAttempt.user_id == user_id)
        .order_by(desc(MockAttempt.completed_at))
        .limit(5)
        .all()
    )

    # Recent dynamic attempts
    recent_dynamic = (
        db.query(DynamicAttempt)
        .filter(DynamicAttempt.user_id == user_id)
        .order_by(desc(DynamicAttempt.created_at))
        .limit(5)
        .all()
    )

    # Recent word similarity
    recent_words = (
        db.query(LevelWord)
        .filter(LevelWord.user_id == user_id)
        .order_by(desc(LevelWord.last_practiced_at))
        .limit(50)
        .all()
    )

    if not recent_mocks and not recent_dynamic and not recent_words:
        return None

    # ---- Mock Average ----
    mock_avg = None
    if recent_mocks:
        scores = [m.total_score for m in recent_mocks if m.total_score is not None]
        if scores:
            mock_avg = round(sum(scores) / len(scores), 2)

    # ---- Dynamic Average ----
    dynamic_avg = None
    if recent_dynamic:
        scores = [d.score for d in recent_dynamic if d.score is not None]
        if scores:
            dynamic_avg = round(sum(scores) / len(scores), 2)

    # ---- Word Similarity Average ----
    similarity_avg = None
    if recent_words:
        sims = [w.last_similarity for w in recent_words if w.last_similarity is not None]
        if sims:
            similarity_avg = round(sum(sims) / len(sims), 2)

    return {
        "mock_average": mock_avg,
        "dynamic_average": dynamic_avg,
        "similarity_average": similarity_avg,
    }
