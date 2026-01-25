# app/mock/routes/report.py

from fastapi import Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.auth.dependencies import get_current_user_id
from app.mock.services.report import generate_mock_report_pdf


def download_mock_report_handler(
    attempt_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),  # 👈 THIS IS AN INT
):
    pdf_buffer = generate_mock_report_pdf(
        db=db,
        user_id=user_id,        # ✅ already an int
        attempt_id=attempt_id
    )

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=mock_report_{attempt_id}.pdf"
        }
    )
