import os
import smtplib
from email.message import EmailMessage


EMAIL_ENABLED = os.getenv("EMAIL_ENABLED", "false").lower() == "true"

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_FROM = os.getenv("SMTP_FROM")


def send_mock_report_email(
    to_email: str,
    subject: str,
    text_body: str,
    html_body: str,
    pdf_bytes: bytes,
    filename: str
):

    if not EMAIL_ENABLED:
        print("📭 Email disabled via .env")
        return

    try:

        msg = EmailMessage()

        msg["Subject"] = subject
        msg["From"] = SMTP_FROM
        msg["To"] = to_email

        msg.set_content(text_body)
        msg.add_alternative(html_body, subtype="html")

        msg.add_attachment(
            pdf_bytes,
            maintype="application",
            subtype="pdf",
            filename=filename
        )

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:

            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)

        print(f"📧 Mock report email sent to {to_email}")

    except Exception as e:
        print("Email sending failed:", str(e))