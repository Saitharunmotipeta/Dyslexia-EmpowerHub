from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.auth.dependencies import get_current_user_id
from app.mock.services.attempt import start_mock_attempt


def start_mock(
    level_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    try:
        # limit = min(limit, len(words))
        return start_mock_attempt(
            db=db,
            user_id=user_id,
            level_id=level_id
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))
        
