from fastapi import HTTPException
from app.practice.services.eval_service import evaluate_similarity
from app.practice.schemas.eval_response import EvaluationResponse


def evaluate_dynamic_text(expected_text: str, recognized_text: str) -> EvaluationResponse:
    expected = (expected_text or "").strip()
    recognized = (recognized_text or "").strip()

    if not expected:
        raise HTTPException(status_code=400, detail="expected_text is required")

    if not recognized:
        raise HTTPException(status_code=400, detail="recognized_text is required")

    score, verdict = evaluate_similarity(expected, recognized)

    return EvaluationResponse(
        word_id=0,
        expected=expected,
        recognized=recognized,
        score=score,
        verdict=verdict,
        is_correct=(score >= 80.0),
    )