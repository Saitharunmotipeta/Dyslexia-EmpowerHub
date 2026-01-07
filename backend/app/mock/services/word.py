from sqlalchemy.orm import Session
from datetime import datetime

from app.mock.models.attempt import MockAttempt
from app.mock.services.evaluate import evaluate_similarity
from app.practice.services.audio_service import convert_to_wav
from app.practice.services.stt_service import speech_to_text
from app.mock.models.word import MockWord


def process_mock_word(
    db: Session,
    user_id: int,
    attempt_id: int,
    word_id: int,
    audio
):
    attempt = db.query(MockAttempt).filter(
        MockAttempt.id == attempt_id,
        MockAttempt.user_id == user_id
    ).first()

    if not attempt:
        raise ValueError("Mock attempt not found")

    if attempt.status == "completed":
        raise ValueError("Mock test already completed")

    # ---- STT PIPELINE ----
    wav_path = convert_to_wav(audio)
    recognized_text = speech_to_text(wav_path)

    expected_text = audio.filename.split(".")[0]  # temporary, frontend-controlled later

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
        "submitted_at": datetime.utcnow().isoformat()
    }

    attempt.results["words"].append(word_result)
    attempt.status = "in_progress"
    attempt.last_accessed_at = datetime.utcnow()

    db.commit()

    # ✅ SCHEMA-COMPLIANT RESPONSE
    return {
        "word_id": word_id,
        "score": evaluation["score"],
        "verdict": evaluation["verdict"],
        "message": "Nice effort! Let’s keep moving 🌱",
        "recognized_text": recognized_text
    }

def get_mock_words_for_level(db: Session, level: str):
    """
    Fetch mock words for a given difficulty level.
    Permanent DB-backed implementation.
    """
    words = (
        db.query(MockWord)
        .filter(MockWord.level == level)
        .all()
    )

    return [
        {
            "id": w.id,
            "word": w.word
        }
        for w in words
    ]

def get_mock_word(db: Session, word_id: int):
    word = db.query(MockWord).filter(MockWord.id == word_id).first()

    return {
        "id": word.id,
        "word": word.word
    }