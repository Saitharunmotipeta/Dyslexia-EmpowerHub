from fastapi import HTTPException
from app.practice.services.eval_service import evaluate_similarity


def evaluate_practice(expected_word: str, recognized_text: str):
    try:
        result = evaluate_similarity(
            expected_word=expected_word,
            recognized_text=recognized_text,
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Evaluation failed")

    return {
        "expected": expected_word,
        "recognized": recognized_text,
        "similarity": result["similarity"],
        "is_correct": result["is_correct"],
    }
