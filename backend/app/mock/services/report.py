from io import BytesIO
from sqlalchemy.orm import Session

from app.mock.models.attempt import MockAttempt
from app.auth.models import User
from app.mock.services.pdf_builder import build_mock_pdf
from app.mock.utils.unlock import can_unlock_next_level

from app.mock.utils.email_service import send_mock_report_email
from app.mock.utils.email_templates import build_mock_report_email


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

    db.refresh(attempt)

    # -----------------------------
    # Fetch user
    # -----------------------------

    user = db.query(User).filter(User.id == attempt.user_id).first()

    username = user.name if user else "User"
    email = user.email if user else None

    # -----------------------------
    # Unlock check
    # -----------------------------

    unlock_info = can_unlock_next_level(
        db=db,
        user_id=user_id,
        public_attempt_id=public_attempt_id
    )

    next_level_unlocked = unlock_info.get("can_proceed", False)

    # -----------------------------
    # Generate PDF
    # -----------------------------

    buffer = build_mock_pdf(
        attempt=attempt,
        username=username,
        next_level_unlocked=next_level_unlocked
    )

    buffer.seek(0)

    # -----------------------------
    # Send email with attachment
    # -----------------------------

    if email:
        _results = attempt.results or {}
        _words = _results.get("words") or []
        _scores = [
            float(w.get("score", 0) or 0)
            for w in _words
            if isinstance(w, dict)
        ]
        if _scores:
            _report_score = round(sum(_scores) / len(_scores), 2)
        else:
            _report_score = attempt.total_score if attempt.total_score else 0

        print("📧 REPORT ATTEMPT ID:", attempt.public_attempt_id)
        print("📊 WORD COUNT:", len(_words))
        print("📊 SCORES:", _scores)
        print("📊 FINAL SCORE:", _report_score)

        subject, text_body, html_body = build_mock_report_email(
            username=username,
            score=_report_score,
            unlocked=next_level_unlocked
        )

        send_mock_report_email(
            to_email=email,
            subject=subject,
            text_body=text_body,
            html_body=html_body,
            pdf_bytes=buffer.getvalue(),
            filename=f"mock-report-{public_attempt_id}.pdf"
        )

    return buffer