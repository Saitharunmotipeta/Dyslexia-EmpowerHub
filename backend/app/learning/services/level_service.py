from sqlalchemy.orm import Session
from typing import List, Tuple

from app.learning.models.level import Level
from app.learning.models.word import Word
from app.learning.models.level_word import LevelWord


def get_levels_with_stats(db: Session, user_id: int) -> List[Tuple[Level, int, int]]:
    """
    Returns list of (level, total_words, mastered_words) for this user.
    """
    print("🔍 Fetching levels with stats for user_id=", user_id)
    levels = db.query(Level).order_by(Level.order).all()
    result = []

    for level in levels:
        print("📂 Processing level_id=", level.id)
        words = db.query(Word).filter(Word.level_id == level.id).all()
        total_words = len(words)

        if total_words == 0:
            mastered_words = 0
        else:
            word_ids = [w.id for w in words]
            mastered_words = (
                db.query(LevelWord)
                .filter(
                    LevelWord.user_id == user_id,
                    LevelWord.word_id.in_(word_ids),
                    LevelWord.is_mastered.is_(True),
                )
                .count()
            )

        print(f"📊 Level {level.id}: total_words={total_words}, mastered_words={mastered_words}")
        result.append((level, total_words, mastered_words))

    print("✅ Levels with stats fetched successfully")
    return result


def get_levels_with_stats_open(db: Session):
    """
    Open version of levels stats (no user-specific mastery).
    Returns (level, total_words, mastered_words=0)
    """
    from sqlalchemy import func, literal

    print("🔓 Fetching open levels with stats")
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
