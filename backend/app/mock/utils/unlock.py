from sqlalchemy.orm import Session
from app.learning.models.level_word import LevelWord
from app.learning.models.level import Level
from app.mock.models.attempt import MockAttempt
from app.learning.models.word import Word
import random
import string

def is_mock_unlocked(
    db: Session,
    user_id: int,
    level_id: int,
) -> bool:
    """
    Unlock mock based on PRACTICE mastery.
    Rule: 70% of words in THIS level mastered.
    """

    # 🔹 Get all words belonging to this level
    words = db.query(Word).filter(
        Word.level_id == level_id
    ).all()

    if not words:
        return False

    word_ids = [w.id for w in words]
    total_words = len(word_ids)

    # 🔹 Count mastered words for this user in this level
    mastered_count = db.query(LevelWord).filter(
        LevelWord.user_id == user_id,
        LevelWord.word_id.in_(word_ids),
        LevelWord.is_mastered.is_(True)
    ).count()

    return (mastered_count / total_words) >= 0.7

# -------------------------------------------------
# MOCK-BASED NEXT LEVEL UNLOCK
# -------------------------------------------------

def can_unlock_next_level(
    db: Session,
    user_id: int,
    public_attempt_id: str
) -> dict:
    """
    Decide whether user can proceed to the NEXT level
    based on mock test score and level difficulty.
    """

    attempt = db.query(MockAttempt).filter(
        MockAttempt.public_attempt_id == public_attempt_id,
        MockAttempt.user_id == user_id
    ).first()

    if not attempt or attempt.total_score is None:
        return {
            "can_proceed": False,
            "reason": "Mock attempt not completed yet"
        }

    level = db.query(Level).filter(
        Level.id == attempt.level_id
    ).first()

    if not level:
        return {
            "can_proceed": False,
            "reason": "Level information not found"
        }

    THRESHOLDS = {
        "easy": 80,
        "medium": 70,
        "hard": 60
    }

    required_score = THRESHOLDS.get(
        level.difficulty.lower(),
        70
    )

    passed = attempt.total_score >= required_score

    return {
        "can_proceed": passed,
        "required_score": required_score,
        "your_score": attempt.total_score,
        "message": (
            "Great job! You’re ready for the next level 🚀"
            if passed
            else f"Score {required_score}% to unlock the next level 💪"
        )
    }


# -------------------------------------------------
# ALPHANUMERIC ATTEMPT CODE GENERATOR
# -------------------------------------------------

def generate_attempt_code(length: int = 8) -> str:
    """
    Public-safe alphanumeric attempt code.
    Example: A7X9Q2LP
    """
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=length))