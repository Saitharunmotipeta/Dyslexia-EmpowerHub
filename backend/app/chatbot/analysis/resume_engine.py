from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import timezone

from app.learning.models.level_word import LevelWord
from app.learning.models.word import Word
from app.learning.models.level import Level
from app.mock.models.attempt import MockAttempt
from app.dynamic.models.dynamic_attempt import DynamicAttempt


MOCK_THRESHOLD = 60
SIMILARITY_THRESHOLD = 60


def normalize(dt):
    if dt is None:
        return None
    if dt.tzinfo is not None:
        return dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt


def format_timestamp(dt):
    if not dt:
        return None
    return dt.strftime("%B %d, %Y at %I:%M %p")


def run(user_id: int, db: Session) -> dict | None:

    # ---- Fetch Latest Word Practice ----
    last_word = (
        db.query(LevelWord)
        .filter(LevelWord.user_id == user_id)
        .order_by(desc(LevelWord.last_practiced_at))
        .first()
    )

    # ---- Fetch Latest Mock ----
    last_mock = (
        db.query(MockAttempt)
        .filter(MockAttempt.user_id == user_id)
        .order_by(desc(MockAttempt.completed_at))
        .first()
    )

    # ---- Fetch Latest Dynamic ----
    last_dynamic = (
        db.query(DynamicAttempt)
        .filter(DynamicAttempt.user_id == user_id)
        .order_by(desc(DynamicAttempt.created_at))
        .first()
    )

    candidates = []

    if last_word and last_word.last_practiced_at:
        candidates.append(("word", normalize(last_word.last_practiced_at), last_word))

    if last_mock:
        ts = last_mock.completed_at or last_mock.started_at
        if ts:
            candidates.append(("mock", normalize(ts), last_mock))

    if last_dynamic:
        candidates.append(("dynamic", normalize(last_dynamic.created_at), last_dynamic))

    if not candidates:
     return {
        "message": "No previous activity found.",
    }

    latest = max(candidates, key=lambda x: x[1])

    activity_type, timestamp, record = latest
    formatted_time = format_timestamp(timestamp)

    # ---- Build Enriched Response ----
    if activity_type == "word":
        word_obj = record.word

        return {
            "summary_type": "activity",
            "activity_type": "word_practice",
            "timestamp": formatted_time,
            "details": {
                "word": word_obj.text if word_obj else None,
                "last_similarity": record.last_similarity,
                "mastery_score": record.mastery_score,
                "is_mastered": record.is_mastered,
                "below_threshold": record.last_similarity < SIMILARITY_THRESHOLD,
            }
        }

    if activity_type == "mock":
        level = record.level

        return {
            "summary_type": "activity",
            "activity_type": "mock_test",
            "timestamp": formatted_time,
            "details": {
                "level_name": level.name if level else None,
                "score": record.total_score,
                "verdict": record.verdict,
                "below_threshold": (
                    record.total_score is not None
                    and record.total_score < MOCK_THRESHOLD
                ),
            }
        }

    if activity_type == "dynamic":
        return {
            "summary_type": "activity",
            "activity_type": "dynamic_practice",
            "timestamp": formatted_time,
            "details": {
                "text": record.text,
                "score": record.score,
                "below_threshold": record.score < MOCK_THRESHOLD,
            }
        }

    return None