from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import timezone

from app.learning.models.level_word import LevelWord
from app.mock.models.attempt import MockAttempt
from app.dynamic.models.dynamic_attempt import DynamicAttempt  # adjust path if needed


def normalize(dt):
    if dt is None:
        return None
    if dt.tzinfo is not None:
        return dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt


def run(user_id: int, db: Session) -> dict | None:

    # Last word practice
    last_word = (
        db.query(LevelWord)
        .filter(LevelWord.user_id == user_id)
        .order_by(desc(LevelWord.last_practiced_at))
        .first()
    )

    # Last mock (prefer completed_at)
    last_mock = (
        db.query(MockAttempt)
        .filter(MockAttempt.user_id == user_id)
        .order_by(desc(MockAttempt.completed_at))
        .first()
    )

    # Last dynamic attempt
    last_dynamic = (
        db.query(DynamicAttempt)
        .filter(DynamicAttempt.user_id == user_id)
        .order_by(desc(DynamicAttempt.created_at))
        .first()
    )

    candidates = []

    if last_word and last_word.last_practiced_at:
        candidates.append(("word_practice", normalize(last_word.last_practiced_at)))

    if last_mock:
        timestamp = last_mock.completed_at or last_mock.started_at
        if timestamp:
            candidates.append(("mock", normalize(timestamp)))

    if last_dynamic:
        candidates.append(("dynamic", normalize(last_dynamic.created_at)))

    if not candidates:
        return None

    latest = max(candidates, key=lambda x: x[1])

    return {
        "last_activity_type": latest[0],
        "last_activity_time": latest[1],
    }
