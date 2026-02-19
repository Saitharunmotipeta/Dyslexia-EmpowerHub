from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.learning.models.level_word import LevelWord
from app.learning.models.word import Word


def run(user_id: int, db: Session) -> dict | None:

    # Find most recently practiced word
    recent_word = (
        db.query(LevelWord)
        .filter(LevelWord.user_id == user_id)
        .order_by(desc(LevelWord.last_practiced_at))
        .first()
    )

    if not recent_word:
        return None

    level_id = recent_word.word.level_id

    # Total words in this level
    total_words = (
        db.query(func.count(Word.id))
        .filter(Word.level_id == level_id)
        .scalar()
    )

    # Mastered words in this level
    mastered_words = (
        db.query(func.count(LevelWord.id))
        .join(Word)
        .filter(
            LevelWord.user_id == user_id,
            Word.level_id == level_id,
            LevelWord.is_mastered == True
        )
        .scalar()
    )

    # Attempted words in this level
    attempted_words = (
        db.query(func.count(LevelWord.id))
        .join(Word)
        .filter(
            LevelWord.user_id == user_id,
            Word.level_id == level_id,
            LevelWord.attempts > 0
        )
        .scalar()
    )

    completion_percent = round((mastered_words / total_words) * 100, 2) if total_words else 0

    return {
        "level_id": level_id,
        "total_words": total_words,
        "attempted_words": attempted_words,
        "mastered_words": mastered_words,
        "completion_percent": completion_percent,
    }
