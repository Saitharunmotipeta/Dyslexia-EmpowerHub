from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy import func
import random

from app.mock.models.attempt import MockAttempt
from app.mock.services.evaluate import evaluate_similarity
from app.learning.models.word import Word


def process_mock_word(
    db: Session,
    user_id: int,
    public_attempt_id: str,  
    word_id: int,
    spoken: str,      
):
    MAX_WORDS = 3

    attempt = db.query(MockAttempt).filter(
        MockAttempt.public_attempt_id == public_attempt_id,
        MockAttempt.user_id == user_id
    ).first()

    if not attempt:
        raise HTTPException(status_code=404, detail="Mock attempt not found")

    if attempt.status == "completed":
        raise HTTPException(status_code=400, detail="Mock test already completed")

    word = db.get(Word, word_id)
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")

    expected_text = word.text

    results = attempt.results or {}
    words = results.get("words", [])

    if any(w["word_id"] == word_id for w in words):
        raise HTTPException(
            status_code=400,
            detail="This word was already submitted"
        )

    if len(words) >= MAX_WORDS:
        raise HTTPException(
            status_code=400,
            detail="All mock words already submitted"
        )

    evaluation = evaluate_similarity(
        expected=expected_text,
        spoken=spoken
    )

    word_result = {
        "word_id": word_id,
        "expected": expected_text,
        "spoken": spoken,
        "score": evaluation["score"],
        "verdict": evaluation["verdict"],
        "phonetics": evaluation.get("phonetics", {}),
        "feedback": evaluation.get("feedback"),
        "submitted_at": datetime.utcnow().isoformat()
    }

    words.append(word_result)

    attempt.results = {
        **results,
        "words": words
    }

    flag_modified(attempt, "results")

    attempt.status = "in_progress"
    attempt.last_accessed_at = datetime.utcnow()

    try:
        db.commit()
        db.refresh(attempt)

    except Exception:
        db.rollback()
        raise

    return {
        "word_id": word_id,
        "score": evaluation["score"],
        "public_attempt_id": public_attempt_id,
        "spoken": spoken,
        "verdict": evaluation["verdict"],
        "recognized_text": spoken,
        "message": "Nice effort! Let’s keep moving 🌱",
    }

def get_mock_words_for_level(
    db: Session,
    level_id: int,
    limit: int = 3
):
    words = (
        db.query(Word)
        .filter(Word.level_id == level_id)
        .order_by(func.random())
        .limit(limit)
        .all()
    )

    return [
        {"id": w.id, "word": w.text}
        for w in words
    ]
