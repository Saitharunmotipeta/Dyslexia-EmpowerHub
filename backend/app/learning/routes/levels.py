from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List

from app.learning.models.level import Level
from app.learning.models.word import Word
from app.learning.models.level_word import LevelWord
from app.mock.models.attempt import MockAttempt
from app.mock.utils.unlock import can_unlock_next_level

from app.learning.schemas.level import LevelOut
from app.learning.schemas.word import WordStatusOut as WordOut


# -------------------------------------------------
# GET ALL LEVELS (USER-SPECIFIC WITH UNLOCK LOGIC)
# -------------------------------------------------

def get_levels_handler(db: Session, user_id: int) -> List[LevelOut]:
    levels = db.query(Level).order_by(Level.order).all()
    result = []

    if not levels:
        return []

    unlocked_levels = set()

    first_level = db.query(Level).order_by(Level.id.asc()).first()
    if first_level:
        unlocked_levels.add(first_level.id)

    # Fetch completed mock attempts
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

        if unlock_info.get("can_proceed"):
            current_level = db.query(Level).filter(
                Level.id == attempt.level_id
            ).first()

            if current_level:
                next_level = db.query(Level).filter(
                    Level.order == current_level.order + 1
                ).first()

                if next_level:
                    unlocked_levels.add(next_level.id)

    for level in levels:
        words = db.query(Word).filter(
            Word.level_id == level.id
        ).all()

        total = len(words)

        if total == 0:
            mastered_words = 0
            mastered_percentage = 0.0
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
                (mastered_words / total) * 100,
                2
            )

        result.append(
            LevelOut(
                id=level.id,
                name=level.name,
                description=level.description or "",
                difficulty=level.difficulty or "",
                order=level.order or 0,
                total_words=total,
                mastered_words=mastered_words,
                mastered_percentage=mastered_percentage,
                is_unlocked=(level.id in unlocked_levels)
            )
        )
    return result



def get_words_for_level_handler(
    level_id: int,
    db: Session,
    user_id: int
):

    level_id = int(level_id)

    levels = get_levels_handler(db, user_id)
    level_map = {lvl.id: lvl for lvl in levels}

    if level_id not in level_map:
        raise HTTPException(status_code=404, detail="Level not found")

    if not level_map[level_id].is_unlocked:
        raise HTTPException(
            status_code=403,
            detail={
                "error": "level_locked",
                "message": "Please complete the previous level to unlock this one.",
                "next_action": "complete_mock"
            }
        )
    # 📚 Fetch words
    words = db.query(Word).filter(
        Word.level_id == level_id
    ).all()

    word_ids = [w.id for w in words]

    progress_rows = (
        db.query(LevelWord)
        .filter(
            LevelWord.user_id == user_id,
            LevelWord.word_id.in_(word_ids)
        )
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
                syllables=w.syllables,
                difficulty=w.difficulty,
                is_mastered=lw.is_mastered if lw else False,
                mastery_score=lw.mastery_score if lw else 0.0,
                attempts=lw.attempts if lw else 0,
            )
        )

    return result