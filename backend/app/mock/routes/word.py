from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.auth.dependencies import get_current_user_id
from app.mock.services.word import process_mock_word
from app.mock.schemas.word import MockWordRequest, MockWordResponse


def submit_mock_word(
    payload: MockWordRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
) -> MockWordResponse:
    """
    Accepts mock word attempt from browser (text-only),
    validates payload via schema, and processes evaluation.
    """

    print("\n📨 MOCK WORD SUBMISSION RECEIVED")
    print("🗣️ Spoken =", payload.spoken)

    result = process_mock_word(
        db=db,
        user_id=user_id,
        attempt_id=payload.attempt_id,
        word_id=payload.word_id,
        spoken=payload.spoken
    )

    # Align response with schema
    return {
        "word_id": payload.word_id,
        "attempt_id": payload.attempt_id,
        "spoken": payload.spoken,
        "score": result["score"],
        "verdict": result["verdict"],
        "message": result["message"],
        "recognized_text": payload.spoken
    }
