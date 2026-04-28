from fastapi import HTTPException, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.auth.dependencies import get_current_user_id
from app.learning.models.word import Word
from app.learning.models.level_word import LevelWord
from app.practice.services.eval_service import evaluate_similarity
from app.practice.services.speech_client import recognize_speech
from app.practice.schemas.eval_response import EvaluationResponse


def evaluate_practice(
    word_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
) -> EvaluationResponse:
    """
    PRACTICE = AUDIO → SPEECH → EVALUATION + TRACKING
    """
    # print("asdfg")

    # -------------------------
    # 1️⃣ Fetch word
    # -------------------------
    word = db.query(Word).filter(Word.id == word_id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    expected = word.text

    # -------------------------
    # 2️⃣ Speech recognition
    # -------------------------
    try:
        file.file.seek(0, 2)
        audio_size = file.file.tell()
        file.file.seek(0)
    except Exception:
        audio_size = -1
    if audio_size == 0:
        raise HTTPException(
            status_code=400,
            detail="Empty audio upload. Record again and ensure the browser has microphone access.",
        )

    try:
        # print("asdfgh")
        speech_result = recognize_speech(file)
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Speech recognition failed: {e!s}",
        ) from e

    spoken = (
        speech_result.get("recognized_text")
        or speech_result.get("text")
        or speech_result.get("transcript")
        or ""
    )
    if isinstance(spoken, str):
        spoken = spoken.strip()
    else:
        spoken = str(spoken or "")

    # -------------------------
    # 3️⃣ Evaluate similarity
    # -------------------------
    score, verdict = evaluate_similarity(expected, spoken)

    # -------------------------
    # 4️⃣ Track user progress
    # -------------------------
    level_word = (
        db.query(LevelWord)
        .filter(
            LevelWord.user_id == user_id,
            LevelWord.word_id == word.id,
        )
        .first()
    )

    if not level_word:
        level_word = LevelWord(
            user_id=user_id,
            word_id=word.id,
            attempts=0,
            correct_attempts=0,
            mastery_score=0.0,
            highest_score=0.0,
            is_mastered=False,
        )
        db.add(level_word)

    level_word.attempts += 1

    if score >= 80:
        level_word.correct_attempts += 1

    level_word.mastery_score = round(
        level_word.correct_attempts / level_word.attempts, 2
    )

    if score > (level_word.highest_score or 0):
        level_word.highest_score = score

    level_word.is_mastered = level_word.highest_score >= 80

    db.commit()

    # -------------------------
    # 5️⃣ Response
    # -------------------------
    return EvaluationResponse(
        word_id=word.id,
        expected=expected,
        recognized=spoken,
        score=score,
        verdict=verdict,
        is_correct=(score >= 80.0),
    )