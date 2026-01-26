from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.auth.dependencies import get_current_user_id
from app.learning.models.word import Word
from app.practice.schemas.eval_schema import EvaluationRequest
from app.practice.schemas.eval_response import EvaluationResponse
from app.practice.services.eval_service import evaluate_similarity


def evaluate_practice(
    payload: EvaluationRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
) -> EvaluationResponse:
    """
    PRACTICE = PURE EVALUATION
    - Auth required
    - No DB mutation
    - User context enforced
    """

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
        verdict=verdict,
        is_correct=(score >= 80.0),
    )
