from sqlalchemy.orm import Session

from app.learning.models.word import Word
from app.learning.models.level_word import LevelWord


def get_words_for_level(db: Session, user_id: int, level_id: int):
    """
    Returns words in a level along with user-specific learning status.
    """
    print("🔍 Fetching words for level_id =", level_id, "user_id =", user_id)

    words = db.query(Word).filter(Word.level_id == level_id).all()
    word_ids = [w.id for w in words]

    level_word_map = {
        lw.word_id: lw
        for lw in db.query(LevelWord)
        .filter(
            LevelWord.user_id == user_id,
            # LevelWord.level_id == level_id,
            LevelWord.word_id.in_(word_ids),
        )
        .all()
    }

    result = []

    for w in words:
        lw = level_word_map.get(w.id)

        attempts = lw.attempts if lw else 0
        mastery_score = lw.mastery_score if lw else 0.0
        is_mastered = lw.is_mastered if lw else False

        print(
            f"📘 Word={w.text} | attempts={attempts} | score={mastery_score} | mastered={is_mastered}"
        )

        result.append(
            {
                "id": w.id,
                "text": w.text,
                "phonetics": w.phonetics,
                "syllables": w.syllables,
                "difficulty": w.difficulty,
                # "image_url": w.image_url,
                "is_mastered": is_mastered,
                "mastery_score": mastery_score,
                "attempts": attempts,
            }
        )

    print("✅ Words fetched successfully for level_id =", level_id)
    return result

def get_words_for_level_open(db: Session, level_id: int):
    """
    Open version of words in a level (no mastery, no attempts).
    """
    print("🔓 Fetching open words for level_id=", level_id)
    return db.query(Word).filter(Word.level_id == level_id).all()
