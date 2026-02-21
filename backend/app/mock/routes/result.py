from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.auth.dependencies import get_current_user_id
from app.mock.services.attempt import finalize_mock_attempt
from app.mock.schemas.result import MockResultRequest, MockResultResponse


def get_mock_result(
    payload: MockResultRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
) -> MockResultResponse:
    """
    Finalizes a mock attempt and returns aggregated result.
    """

    try:
        return finalize_mock_attempt(
            db=db,
            user_id=user_id,
            public_attempt_id=payload.public_attempt_id,
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        print("result route passed")
