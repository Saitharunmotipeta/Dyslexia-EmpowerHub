# app/mock/services/automation.py

import random
from sqlalchemy.orm import Session

from app.mock.models.attempt import MockAttempt
from app.mock.models.word import MockWord
from app.mock.services.word import process_mock_word
from app.mock.services.attempt import finalize_mock_attempt
from app.mock.utils.unlock import can_unlock_next_level


# -------------------------------------------------
# Utilities
# -------------------------------------------------

def generate_attempt_code() -> str:
    """
    Public-safe attempt code.
    Example: MOCK-482193
    """
    return f"MOCK-{random.randint(0, 999999):06d}"


# -------------------------------------------------
# Automation Core
# -------------------------------------------------

def start_mock_automation(
    db: Session,
    user_id: int,
    level_id: int,
):
    """
    Starts automated mock test.
    """

    # -----------------------------
    # Unlock rule
    # -----------------------------

    if not can_unlock_next_level(db, user_id, level_id):
        raise ValueError(
            "Mock test is still locked. Practice a few more words to unlock it."
        )

    # -----------------------------
    # Fetch mock words
    # -----------------------------

    words = (
        db.query(MockWord)
        .filter(MockWord.level_id == level_id)
        .all()
    )

    if len(words) < 3:
        raise ValueError(
            "Not enough mock words available for this level."
        )

    selected_words = random.sample(words, 3)

    # -----------------------------
    # Unique attempt id
    # -----------------------------

    public_attempt_id = generate_attempt_code()

    while db.query(MockAttempt).filter(
        MockAttempt.public_attempt_id == public_attempt_id
    ).first():
        public_attempt_id = generate_attempt_code()

    # -----------------------------
    # Create attempt
    # -----------------------------

    attempt = MockAttempt(
        user_id=user_id,
        level_id=level_id,
        public_attempt_id=public_attempt_id,
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
                "text": w.word
            }
            for w in selected_words
        ],
        "message": "Mock test started. Speak each word clearly and take your time 🌱"
    }


# -------------------------------------------------
# Submit Word
# -------------------------------------------------

def submit_mock_word_automation(
    db: Session,
    user_id: int,
    public_attempt_id: str,
    word_id: int,
    audio,
):
    """
    Submit audio for one word during automated mock.
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
        raise ValueError("This mock test has already been completed.")

    submitted_words = {
        w["word_id"]
        for w in attempt.results.get("words", [])
    }

    if word_id in submitted_words:
        raise ValueError(
            "This word has already been submitted."
        )

    # reuse main processing logic
    return process_mock_word(
        db=db,
        user_id=user_id,
        public_attempt_id=public_attempt_id,
        word_id=word_id,
        audio=audio,
    )


# -------------------------------------------------
# Complete Mock
# -------------------------------------------------

def complete_mock_automation(
    db: Session,
    user_id: int,
    public_attempt_id: str,
):
    """
    Finalizes automated mock.
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
            "Please submit all three words before completing the mock test."
        )

    return finalize_mock_attempt(
        db=db,
        user_id=user_id,
        public_attempt_id=public_attempt_id,
    )