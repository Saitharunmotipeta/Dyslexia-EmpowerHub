# app/mock/routes/automation.py

from fastapi import UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.auth.dependencies import get_current_user_id
from app.mock.services.automation import (
    start_mock_automation,
    submit_mock_word_automation,
    complete_mock_automation,
)


def start_automation(
    level_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """
    Start automated mock test.
    Returns attempt_code + selected words.
    """
    try:
        return start_mock_automation(
            db=db,
            user_id=user_id,
            level_id=level_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))


def submit_word_automation(
    attempt_code: int,
    word_id: int,
    audio: UploadFile = File(...),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """
    Submit audio for a word during mock automation.
    Called exactly 3 times (once per word).
    """
    try:
        return submit_mock_word_automation(
            db=db,
            user_id=user_id,
            attempt_code=attempt_code,
            word_id=word_id,
            audio=audio,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


def complete_automation(
    attempt_code: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """
    Finalize automated mock test.
    Aggregates score + verdict.
    """
    try:
        return complete_mock_automation(
            db=db,
            user_id=user_id,
            attempt_code=attempt_code,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
