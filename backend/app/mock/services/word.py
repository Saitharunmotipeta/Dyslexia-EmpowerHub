from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm.attributes import flag_modified
from pathlib import Path
import random
from sqlalchemy import func
import uuid
import shutil

from app.mock.models.attempt import MockAttempt
from app.mock.services.evaluate import evaluate_similarity
from app.practice.services.audio_service import convert_to_wav, UPLOAD_DIR
from app.practice.services.stt_service import speech_to_text
from app.learning.models.word import Word


# -------------------------------
# AUDIO SAVE HELPER
# -------------------------------

def save_upload_with_id(audio, user_id: int) -> str:
    """
    Save UploadFile to UPLOAD_DIR using a generated file_id.
    Returns file_id (without extension).
    """
    file_id = str(uuid.uuid4())
    ext = Path(audio.filename).suffix or ".webm"

    user_dir = UPLOAD_DIR / str(user_id)
    user_dir.mkdir(parents=True, exist_ok=True)

    dest = user_dir / f"{file_id}{ext}"

    with dest.open("wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)

    return file_id


# -------------------------------
# PROCESS MOCK WORD
# -------------------------------

def process_mock_word(
    db: Session,
    user_id: int,
    attempt_id: int,   # attempt_code (public-facing)
    word_id: int,
    audio
):
    MAX_WORDS = 3

    # 1️⃣ Fetch attempt
    attempt = db.query(MockAttempt).filter(
        MockAttempt.attempt_code == attempt_id,
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

    # 3️⃣ Prepare results container safely
    results = attempt.results or {}
    words = results.get("words", [])

    # 🚫 Duplicate word protection
    if any(w["word_id"] == word_id for w in words):
        raise HTTPException(
            status_code=400,
            detail="This word was already submitted for this attempt"
        )

    # 🚫 Max words protection
    if len(words) >= MAX_WORDS:
        raise HTTPException(
            status_code=400,
            detail="All mock words already submitted"
        )

    # 4️⃣ STT pipeline
    file_id = save_upload_with_id(audio, user_id)
    wav_path = convert_to_wav(file_id, user_id)
    recognized_text = speech_to_text(wav_path)["text"]

    # 5️⃣ Evaluate pronunciation
    evaluation = evaluate_similarity(
        expected=expected_text,
        spoken=recognized_text
    )

    word_result = {
        "word_id": word_id,
        "expected": expected_text,
        "recognized": recognized_text,
        "score": evaluation["score"],
        "verdict": evaluation["verdict"],
        "phonetics": evaluation.get("phonetics", {}),
        "feedback": evaluation.get("feedback"),
        "submitted_at": datetime.utcnow().isoformat()
    }

    # 6️⃣ Append + FORCE SQLAlchemy to persist JSON
    words.append(word_result)

    attempt.results = {
        **results,
        "words": words
    }

    flag_modified(attempt, "results")  # 🔥 THIS IS CRITICAL

    attempt.status = "in_progress"
    attempt.last_accessed_at = datetime.utcnow()

    # 7️⃣ Commit safely
    try:
        db.commit()
        db.refresh(attempt)
    except Exception:
        db.rollback()
        raise

    # 8️⃣ API response
    return {
        "word_id": word_id,
        "score": evaluation["score"],
        "verdict": evaluation["verdict"],
        "message": "Nice effort! Let’s keep moving 🌱",
        "recognized_text": recognized_text
    }
# def get_mock_word(db: Session, word_id: int):
#     word = db.query(MockWord).filter(MockWord.id == word_id).first()

#     return {
#         "id": word.id,
#         "word": word.word
#     }

def get_mock_words_for_level(
    db: Session,
    level_id: int,
    limit: int = 3
):
    words = (
        db.query(Word)
        .filter(Word.level_id == level_id)
        .order_by(func.random())   # ✅ KEY LINE
        .limit(limit)
        .all()
    )
    rows = words
    return [
        {
            "id": w.id,
            "word": w.text
        }
        for w in rows   # ✅ FIX
    ]