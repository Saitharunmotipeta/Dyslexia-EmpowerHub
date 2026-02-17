from sqlalchemy.orm import Session
from app.learning.models.level_word import LevelWord
from app.learning.models.level import Level
from app.mock.models.attempt import MockAttempt
import random


# -------------------------------------------------
# PRACTICE-BASED UNLOCK (OLD LOGIC, STILL VALID)
# -------------------------------------------------

def is_mock_unlocked(
    db: Session,
    user_id: int,
    # level_id: int
) -> bool:
    """
    Unlock mock based on PRACTICE mastery.
    Rule: 70% of level words mastered.
    """

    total = db.query(LevelWord).filter(
        LevelWord.user_id == user_id,
        # LevelWord.level_id == level_id
    ).count()

    if total == 0:
        return False

    mastered = db.query(LevelWord).filter(
        LevelWord.user_id == user_id,
        # LevelWord.level_id == level_id,
        LevelWord.is_mastered.is_(True)
    ).count()

    return (mastered / total) >= 0.7


# -------------------------------------------------
# MOCK-BASED NEXT LEVEL UNLOCK (NEW)
# -------------------------------------------------

def can_unlock_next_level(
    db: Session,
    user_id: int,
    attempt_code: int
) -> dict:
    """
    Decide whether user can proceed to the NEXT level
    based on mock test score and level difficulty.
    """

    attempt = db.query(MockAttempt).filter(
        MockAttempt.attempt_code == attempt_code,
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

    # 🎯 Thresholds (easy to tune later)
    THRESHOLDS = {
        "easy": 80,
        "medium": 70,
        "hard": 60
    }

    required_score = THRESHOLDS.get(
        level.difficulty.lower(),
        70  # safe default
    )

    passed = attempt.total_score >= required_score

    return {
        "can_proceed": passed,
        "required_score": required_score,
        "your_score": attempt.total_score,
        "message": (
            "Great job! You’re ready for the next level 🚀"
            if passed
            else
            f"Almost there! Score {required_score}% to unlock the next level 💪"
        )
    }


# -------------------------------------------------
# ATTEMPT CODE GENERATOR
# -------------------------------------------------

def generate_attempt_code() -> int:
    """
    Public-safe 6 digit attempt code
    """
    return random.randint(100000, 999999)
