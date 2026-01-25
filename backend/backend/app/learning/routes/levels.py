# app/learning/routes/levels.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List

from app.learning.models.level import Level
from app.learning.models.word import Word
from app.learning.models.level_word import LevelWord

from app.learning.schemas.level import LevelOut
from app.learning.schemas.word import WordStatusOut as WordOut


def get_levels_handler(db: Session) -> List[LevelOut]:
    levels = db.query(Level).order_by(Level.order).all()
    result = []

    for level in levels:
        words = db.query(Word).filter(Word.level_id == level.id).all()
        total = len(words)

        result.append(
            LevelOut(
                id=level.id,
                name=level.name,
                description=level.description or "",
                difficulty=level.difficulty or "",
                order=level.order or 0,
                total_words=total,
                mastered_words=0,
                mastered_percentage=0
            )
        )

    return result


def get_words_for_level_handler(level_id: int, db: Session, user_id: int):

    level = db.query(Level).filter(Level.id == level_id).first()
    if not level:
        raise HTTPException(status_code=404, detail="Level not found")

    words = db.query(Word).filter(Word.level_id == level_id).all()
    word_ids = [w.id for w in words]

    progress_rows = (
        db.query(LevelWord)
        .filter(LevelWord.user_id == user_id,
                LevelWord.word_id.in_(word_ids))
        .all()
    )

    progress_map = {row.word_id: row for row in progress_rows}

    result = []

    for w in words:
        lw = progress_map.get(w.id)

        result.append(
            WordOut(
                id=w.id,
                text=w.text,
                phonetics=w.phonetics,

                # 🔥 REQUIRED FIELDS — these FIX the 500 error
                syllables=w.syllables,
                difficulty=w.difficulty,

                image_url=w.image_url,
                is_mastered=lw.is_mastered if lw else False,
                mastery_score=lw.mastery_score if lw else 0.0,
                attempts=lw.attempts if lw else 0,
            )
        )

    return result
