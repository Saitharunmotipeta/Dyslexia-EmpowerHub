# app/mock/services/automation.py

import random
from sqlalchemy.orm import Session

from app.mock.models.attempt import MockAttempt
from app.mock.services.word import process_mock_word
from app.mock.services.attempt import finalize_mock_attempt
from app.learning.models.word import Word
from app.mock.utils.unlock import can_unlock_next_level


# -------------------------------------------------
# Utilities
# -------------------------------------------------

def generate_attempt_code() -> int:
    """
    Public-safe 6 digit attempt code.
    Example: 042931
    """
    return int(f"{random.randint(0, 999999):06d}")


# -------------------------------------------------
# Automation Core
# -------------------------------------------------

def start_mock_automation(
    db: Session,
    user_id: int,
    level_id: int,
):
    """
    Starts automated mock.
    - Unlock-aware
    - Returns attempt_code + words
    """

    # 1️⃣ Unlock rule
    if not can_unlock_next_level(db, user_id, level_id):
        raise ValueError(
            "Mock test is locked. Practice a few more words to unlock."
        )

    # 2️⃣ Fetch words
    words = (
        db.query(Word)
        .filter(Word.level_id == level_id)
        .all()
    )

    if len(words) < 3:
        raise ValueError("Not enough words to start mock test.")

    selected_words = random.sample(words, 3)

    # 3️⃣ Create attempt
    attempt = MockAttempt(
        user_id=user_id,
        level_id=level_id,
        public_attempt_id=generate_attempt_code(),
        status="started",
        results={"words": []},
    )

    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    return {
        "public_attempt_id": attempt.public_attempt_id,
        "words": [
            {
                "word_id": w.id,
                "text": w.text
            }
            for w in selected_words
        ]
    }


def submit_mock_word_automation(
    db: Session,
    user_id: int,
    public_attempt_id: str,
    word_id: int,
    audio,
):
    """
    Submit a single word audio during automation.
    """

    attempt = (
        db.query(MockAttempt)
        .filter(
            MockAttempt.public_attempt_id == public_attempt_id,
            MockAttempt.user_id == user_id
        )
        .first()
    )

    if not attempt:
        raise ValueError("Invalid mock attempt.")

    if attempt.status == "completed":
        raise ValueError("Mock test already completed.")

    submitted_words = {
        w["word_id"]
        for w in attempt.results.get("words", [])
    }

    if word_id in submitted_words:
        raise ValueError("This word has already been submitted.")

    # 🔁 Reuse SAME logic as manual mock
    return process_mock_word(
        db=db,
        user_id=user_id,
        public_attempt_id=public_attempt_id,   # public-safe key
        word_id=word_id,
        audio=audio,
    )


def complete_mock_automation(
    db: Session,
    user_id: int,
    public_attempt_id: str,
):
    """
    Finalize automated mock.
    """

    attempt = (
        db.query(MockAttempt)
        .filter(
            MockAttempt.public_attempt_id == public_attempt_id,
            MockAttempt.user_id == user_id
        )
        .first()
    )

    if not attempt:
        raise ValueError("Invalid mock attempt.")

    words = attempt.results.get("words", [])

    if len(words) < 3:
        raise ValueError(
            "Submit all 3 words before completing mock test."
        )

    # 🔁 Reuse SAME finalization logic
    return finalize_mock_attempt(
        db=db,
        user_id=user_id,
        public_attempt_id=public_attempt_id,
    )
