from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.auth.dependencies import get_current_user_id
from app.mock.services.attempt import finalize_mock_attempt


def get_mock_result(
    attempt_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    try:
        return finalize_mock_attempt(
            db=db,
            user_id=user_id,
            attempt_id=attempt_id
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
