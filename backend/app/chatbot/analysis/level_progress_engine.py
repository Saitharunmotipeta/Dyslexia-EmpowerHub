from sqlalchemy.orm import Session
from sqlalchemy import func, desc, asc

from app.learning.models.level_word import LevelWord
from app.learning.models.word import Word
from app.learning.models.level import Level


def run(user_id: int, db: Session, level_order: int | None = None):

    # -------------------------------------------------
    # 1️⃣ Determine Target Level
    # -------------------------------------------------

    if level_order:
        level = (
            db.query(Level)
            .filter(Level.order == level_order)
            .first()
        )
        if level_order is None:
            return {
        "error": "level_not_specified"
    }
    else:
        # fallback: use most recently practiced level
        recent_word = (
            db.query(LevelWord)
            .filter(LevelWord.user_id == user_id)
            .order_by(desc(LevelWord.last_practiced_at))
            .first()
        )

        if not recent_word:
            return {
                "error": "no_recent_word_found"
            }

        level = recent_word.word.level

    if not level:
        return {
            "error": "level_not_found"}

    # -------------------------------------------------
    # 2️⃣ Compute Level Statistics
    # -------------------------------------------------

    total_words = (
        db.query(func.count(Word.id))
        .filter(Word.level_id == level.id)
        .scalar()
    )

    mastered_words = (
        db.query(func.count(LevelWord.id))
        .join(Word)
        .filter(
            LevelWord.user_id == user_id,
            Word.level_id == level.id,
            LevelWord.is_mastered == True
        )
        .scalar()
    )

    attempted_words = (
        db.query(func.count(LevelWord.id))
        .join(Word)
        .filter(
            LevelWord.user_id == user_id,
            Word.level_id == level.id,
            LevelWord.attempts > 0
        )
        .scalar()
    )

    remaining_words = total_words - mastered_words if total_words else 0

    completion_percent = (
        round((mastered_words / total_words) * 100, 2)
        if total_words else 0
    )

    # -------------------------------------------------
    # 3️⃣ Practice Recommendation Logic
    # -------------------------------------------------

    recommendation = None

    if mastered_words == total_words:
        # Level mastered → suggest next level
        next_level = (
            db.query(Level)
            .filter(Level.order == level.order + 1)
            .first()
        )

        if next_level:
            recommendation = f"Move to next level: {next_level.name}"
        else:
            recommendation = "All levels mastered. Great work!"
    else:
        # Suggest weakest word in this level
        weakest_word = (
            db.query(LevelWord)
            .join(Word)
            .filter(
                LevelWord.user_id == user_id,
                Word.level_id == level.id
            )
            .order_by(
                asc(LevelWord.is_mastered),
                asc(LevelWord.mastery_score),
                asc(LevelWord.last_similarity)
            )
            .first()
        )

        if weakest_word:
            recommendation = f"Practice word: {weakest_word.word.text}"

    # -------------------------------------------------
    # 4️⃣ Return Structured Deterministic Output
    # -------------------------------------------------

    return {
        "summary_type": "level_specific",
        "level_name": level.name,
        "level_order": level.order,
        "total_words": total_words,
        "attempted_words": attempted_words,
        "mastered_words": mastered_words,
        "remaining_words": remaining_words,
        "completion_percent": completion_percent,
        "recommendation": recommendation,
    }