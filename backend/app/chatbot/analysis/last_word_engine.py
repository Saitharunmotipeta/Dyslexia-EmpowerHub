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
    is_mastered = last_word.is_mastered
    attempts = last_word.attempts

    # Deterministic Recommendation Logic
    if not is_mastered:
        recommendation = f"Practice '{last_word.word.text}' again to improve accuracy."
    elif similarity < PASS_THRESHOLD:
        recommendation = f"Refine pronunciation of '{last_word.word.text}' to cross {PASS_THRESHOLD}%."
    else:
        recommendation = "Move to the next weak word in this level."

    return {
        "word": last_word.word.text,
        "level_id": last_word.word.level_id,
        "last_practiced_at": last_word.last_practiced_at,
        "similarity_percent": similarity,
        "attempts": attempts,
        "is_mastered": is_mastered,
        "below_threshold": similarity < PASS_THRESHOLD,
        "recommendation": recommendation,
    }