from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy import func
import random

from app.mock.models.attempt import MockAttempt
from app.mock.services.evaluate import evaluate_similarity
from app.learning.models.word import Word


# -------------------------------
# PROCESS MOCK WORD (BROWSER STT)
# -------------------------------

def process_mock_word(
    db: Session,
    user_id: int,
    attempt_id: int,   # public attempt_code
    word_id: int,
    spoken: str,       # ✅ FROM BROWSER
):
    MAX_WORDS = 3

    print("\n🧪 MOCK WORD PROCESS STARTED")
    print(f"🆔 Attempt ID = {attempt_id}")
    print(f"📝 Word ID    = {word_id}")
    print(f"🗣️ Spoken     = {spoken}")

    # 1️⃣ Fetch attempt
    attempt = db.query(MockAttempt).filter(
        MockAttempt.public_attempt_id == str(attempt_id),
        MockAttempt.user_id == user_id
    ).first()

    if not attempt:
        raise HTTPException(status_code=404, detail="Mock attempt not found")

    if attempt.status == "completed":
        raise HTTPException(status_code=400, detail="Mock test already completed")

    # 2️⃣ Fetch expected word
    word = db.get(Word, word_id)
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")

    expected_text = word.text
    print(f"📖 Expected = {expected_text}")

    # 3️⃣ Prepare results
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

    # 4️⃣ Evaluate pronunciation (NO STT HERE)
    evaluation = evaluate_similarity(
        expected=expected_text,
        spoken=spoken
    )

    print("📊 Score =", evaluation["score"])
    print("⚖️ Verdict =", evaluation["verdict"])

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
        print("💾 Mock word saved")
    except Exception:
        db.rollback()
        raise

    return {
        "word_id": word_id,
        "score": evaluation["score"],
        "verdict": evaluation["verdict"],
        "recognized_text": spoken,
        "message": "Nice effort! Let’s keep moving 🌱",
    }


# -------------------------------
# FETCH RANDOM MOCK WORDS
# -------------------------------

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
