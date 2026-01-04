from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.learning.models.word import Word
from app.practice.schemas.eval_schema import EvaluationRequest
from app.practice.schemas.eval_response import EvaluationResponse
from app.practice.services.eval_service import evaluate_similarity


def evaluate_practice(payload: EvaluationRequest) -> EvaluationResponse:
    db: Session = SessionLocal()

    try:
        word = db.query(Word).filter(Word.id == payload.word_id).first()
        if not word:
            raise HTTPException(status_code=404, detail="Word not found")

        expected = word.text
        spoken = payload.recognized_text

        score, verdict = evaluate_similarity(expected, spoken)

        return EvaluationResponse(
            word_id=payload.word_id,
            expected=expected,
            recognized=spoken,
            score=score,
            is_correct=(score >= 80.0)  # business rule — tweak later
        )

    finally:
        db.close()
