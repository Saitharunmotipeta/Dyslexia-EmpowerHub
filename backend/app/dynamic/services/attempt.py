import random
import string
from datetime import datetime
from sqlalchemy.orm import Session

from app.dynamic.models.dynamic_attempt import DynamicAttempt


# --------------------------------------------------
# Generate Public Dynamic Attempt ID (DYN-XXXXXX)
# --------------------------------------------------

def generate_dynamic_attempt_id(db: Session) -> str:
    """
    Generate unique ID like DYN-AB12CD
    """

    while True:
        random_part = ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=6)
        )

        public_id = f"DYN-{random_part}"

        exists = db.query(DynamicAttempt).filter(
            DynamicAttempt.public_attempt_id == public_id
        ).first()

        if not exists:
            return public_id


# --------------------------------------------------
# Create Dynamic Attempt
# --------------------------------------------------

def create_dynamic_attempt(
    db: Session,
    user_id: int,
    text: str,
    text_type: str,
    spoken: str,
    score: float,
    pace: float | None
) -> DynamicAttempt:

    public_id = generate_dynamic_attempt_id(db)

    attempt = DynamicAttempt(
        user_id=user_id,
        public_attempt_id=public_id,
        text=text,
        text_type=text_type,
        spoken=spoken,
        score=score,
        pace=pace,
        created_at=datetime.utcnow()
    )

    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    return attempt
