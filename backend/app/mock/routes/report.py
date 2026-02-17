# app/mock/routes/report.py

from fastapi import Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.auth.dependencies import get_current_user_id
from app.mock.services.report import generate_mock_report_pdf
from app.mock.models.attempt import MockAttempt


def mock_report_handler(
    public_attempt_id: str = Query(...),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    """
    Single handler for mock report:
    - Generates PDF internally (for email / future use)
    - Returns JSON preview for frontend
    """

    attempt = db.query(MockAttempt).filter(
        MockAttempt.public_attempt_id == public_attempt_id,
        MockAttempt.user_id == user_id
    ).first()

    if not attempt:
        raise HTTPException(status_code=404, detail="Mock attempt not found")

    if attempt.status != "completed":
        raise HTTPException(
            status_code=400,
            detail="Mock test not completed yet"
        )

    # ✅ Generate PDF (side-effect only)
    pdf_buffer = generate_mock_report_pdf(
        db=db,
        user_id=user_id,
        public_attempt_id=public_attempt_id
    )

    print(f"📄 PDF REPORT GENERATED for attempt_id={public_attempt_id}")
    print(f"📦 PDF size: {len(pdf_buffer.getvalue())} bytes")

    results = attempt.results or {}
    words = results.get("words", [])

    # ✅ JSON preview response
    return {
        "attempt_id": public_attempt_id,
        "final_score": attempt.total_score,
        "verdict": attempt.verdict,
        "words": [
            {
                "expected": w.get("expected"),
                "spoken": w.get("spoken"),
                "score": w.get("score"),
                "verdict": w.get("verdict"),
                "feedback": w.get("feedback"),
            }
            for w in words
        ],
        "pdf_generated": True,
        "message": "Mock report generated successfully"
    }
