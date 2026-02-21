from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.learning.models.level_word import LevelWord


PASS_THRESHOLD = 80


def run(user_id: int, db: Session) -> dict | None:

    last_word = (
        db.query(LevelWord)
        .filter(LevelWord.user_id == user_id)
        .order_by(desc(LevelWord.last_practiced_at))
        .first()
    )

    if not last_word or not last_word.word:
        return None

    similarity = round(last_word.last_similarity or 0, 2)

    return {
        "word": last_word.word.text,
        "level_id": last_word.word.level_id,
        "last_practiced_at": last_word.last_practiced_at,
        "similarity_percent": similarity,
        "attempts": last_word.attempts,
        "is_mastered": last_word.is_mastered,
        "below_threshold": similarity < PASS_THRESHOLD,
    }