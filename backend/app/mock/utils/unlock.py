from sqlalchemy.orm import Session
from app.learning.models.level_word import LevelWord


def is_mock_unlocked(
    db: Session,
    user_id: int,
    level_id: int
) -> bool:
    total = db.query(LevelWord).filter(
        LevelWord.user_id == user_id,
        LevelWord.level_id == level_id
    ).count()

    if total == 0:
        return False

    mastered = db.query(LevelWord).filter(
        LevelWord.user_id == user_id,
        LevelWord.level_id == level_id,
        LevelWord.is_mastered.is_(True)
    ).count()

    return (mastered / total) >= 0.7
