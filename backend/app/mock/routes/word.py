from fastapi import UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.practice.services.audio_service import UPLOAD_DIR


from app.database.connection import get_db
from app.auth.dependencies import get_current_user_id
from app.mock.services.word import process_mock_word


def submit_mock_word(
    attempt_id: int,
    word_id: int,
    audio: UploadFile = File(...),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    try:
        return process_mock_word(
            db=db,
            user_id=user_id,
            attempt_id=attempt_id,
            word_id=word_id,
            audio=audio
        )
    # except ValueError as e:
    #     raise HTTPException(status_code=400, detail=str(e))
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))
    finally:
        print("submit")