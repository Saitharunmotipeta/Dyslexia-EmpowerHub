from io import BytesIO
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.mock.models.attempt import MockAttempt
from app.auth.models import User
from app.mock.services.pdf_builder import build_mock_pdf
from app.mock.utils.unlock import can_unlock_next_level


def generate_mock_report_pdf(
    db: Session,
    user_id: int,
    public_attempt_id: str
) -> BytesIO:

    attempt = db.query(MockAttempt).filter(
        MockAttempt.public_attempt_id == public_attempt_id
    ).first()

    if not attempt:
        raise FileNotFoundError("Mock attempt not found")

    if attempt.user_id != user_id:
        raise PermissionError("Access denied")

    if attempt.status != "completed":
        raise ValueError("Mock test not completed yet")

    # Fetch username
    user = db.query(User).filter(User.id == attempt.user_id).first()
    username = user.name if user else "Unknown"

    # Check unlock eligibility
    unlock_info = can_unlock_next_level(
        db=db,
        user_id=user_id,
        public_attempt_id=public_attempt_id
    )

    next_level_unlocked = unlock_info.get("can_proceed", False)

    # Build PDF in memory
    buffer = build_mock_pdf(
        attempt=attempt,
        username=username,
        next_level_unlocked=next_level_unlocked
    )

    # Reset buffer pointer (important for reading later)
    buffer.seek(0)

    return buffer