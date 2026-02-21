from fastapi import HTTPException, Depends, Query
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.auth.dependencies import get_current_user_id
from app.mock.services.attempt import start_mock_attempt
from app.mock.schemas.start import MockStartResponse


def start_mock(
    level_id: int = Query(..., description="Level ID for mock test"),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
) -> MockStartResponse:
    """
    Starts a mock test for a given level.
    Returns a public attempt_id and the selected mock words.
    """

    try:
        return start_mock_attempt(
            db=db,
            user_id=user_id,
            level_id=level_id
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
