from fastapi import Depends, HTTPException, Body
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.auth.dependencies import get_current_user_id
from app.mock.services.word import process_mock_word


def submit_mock_word(
    attempt_id: int,
    word_id: int,
    spoken: str = Body(..., embed=True),  # ✅ BROWSER STT TEXT
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    print("\n📨 MOCK WORD SUBMISSION RECEIVED")
    print("🗣️ Spoken =", spoken)

    return process_mock_word(
        db=db,
        user_id=user_id,
        attempt_id=attempt_id,
        word_id=word_id,
        spoken=spoken
    )
