from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.auth.dependencies import get_current_user_id

from app.dynamic.schemas import DynamicAttemptCreate, DynamicAttemptOut
from app.dynamic.services.attempt import create_dynamic_attempt


def save_dynamic_attempt(
    data: DynamicAttemptCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
) -> DynamicAttemptOut:

    """
    Saves a dynamic attempt from the user.
    
    Args:
        data: DynamicAttemptCreate - The data to save.
        db: Session - The database session.
        user_id: int - The user ID.
    
    Returns:
        DynamicAttemptOut - The saved attempt data.
    
    Raises:
        HTTPException - If the data is invalid.
    """
    if not data.text or not data.spoken:
        raise HTTPException(status_code=400, detail="Invalid attempt data")

    attempt = create_dynamic_attempt(
        db=db,
        user_id=user_id,
        text=data.text,
        text_type=data.text_type,
        spoken=data.spoken,
        score=data.score,
        pace=data.pace
    )

    return DynamicAttemptOut(
        attempt_id=attempt.public_attempt_id,
        message="Dynamic attempt saved successfully"
    )
