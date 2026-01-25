# app/learning/routes/words.py
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.learning.models.word import Word
from app.learning.models.level_word import LevelWord


def update_word_status_handler(
    db: Session,
    user_id: int,
    word_id: int,
    is_mastered: bool,
    mastery_score: float,
):
    word = db.query(Word).filter(Word.id == word_id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")

    record = (
        db.query(LevelWord)
        .filter(
            LevelWord.user_id == user_id,
            LevelWord.word_id == word_id,
            LevelWord.level_id == word.level_id,
        )
        .first()
    )

    if not record:
        record = LevelWord(
            user_id=user_id,
            word_id=word_id,
            level_id=word.level_id,
        )
        db.add(record)

    record.mastery_score = mastery_score
    record.is_mastered = is_mastered

    db.commit()
    db.refresh(record)

    return {
        "message": "Learning progress updated",
        "word_id": word_id,
        "is_mastered": record.is_mastered,
        "mastery_score": record.mastery_score,
    }
