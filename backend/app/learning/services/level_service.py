from sqlalchemy.orm import Session
from typing import List, Tuple, Dict

from app.learning.models.level import Level
from app.learning.models.word import Word
from app.learning.models.level_word import LevelWord
from app.mock.models.attempt import MockAttempt
from app.mock.utils.unlock import can_unlock_next_level


def get_levels_with_stats(db: Session, user_id: int) -> List[Dict]:

    levels = db.query(Level).order_by(Level.order).all()
    result = []

    unlocked_levels = set()

    if not levels:
        return []

    first_level = levels[0]
    unlocked_levels.add(first_level.id)

    completed_attempts = db.query(MockAttempt).filter(
        MockAttempt.user_id == user_id,
        MockAttempt.status == "completed"
    ).all()

    for attempt in completed_attempts:
        unlock_info = can_unlock_next_level(
            db=db,
            user_id=user_id,
            public_attempt_id=attempt.public_attempt_id
        )

        if unlock_info["can_proceed"]:
            current_level = attempt.level_id

            next_level = db.query(Level).filter(
                Level.order == (
                    db.query(Level.order)
                    .filter(Level.id == current_level)
                    .scalar()
                ) + 1
            ).first()

            if next_level:
                unlocked_levels.add(next_level.id)

    for level in levels:

        words = db.query(Word).filter(
            Word.level_id == level.id
        ).all()

        total_words = len(words)

        if total_words == 0:
            mastered_words = 0
            mastered_percentage = 0
        else:
            word_ids = [w.id for w in words]

            mastered_words = (
                db.query(LevelWord)
                .filter(
                    LevelWord.user_id == user_id,
                    LevelWord.word_id.in_(word_ids),
                    LevelWord.is_mastered.is_(True)
                )
                .count()
            )

            mastered_percentage = round(
                (mastered_words / total_words) * 100,
                2
            )

        result.append({
            "id": level.id,
            "name": level.name,
            "description": level.description,
            "difficulty": level.difficulty,
            "order": level.order,
            "total_words": total_words,
            "mastered_words": mastered_words,
            "mastered_percentage": mastered_percentage,
            "is_unlocked": level.id in unlocked_levels
        })

    return result

def get_levels_with_stats_open(db: Session):
    """
    Open version of levels stats (no user-specific mastery).
    Returns (level, total_words, mastered_words=0)
    """
    from sqlalchemy import func, literal
    return (
        db.query(
            Level,
            func.count(Word.id).label("total_words"),
            literal(0).label("mastered_words"),
        )
        .join(Word, Word.level_id == Level.id)
        .group_by(Level.id)
        .order_by(Level.order)
        .all()
    )
