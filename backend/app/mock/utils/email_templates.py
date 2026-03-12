def build_mock_report_email(username: str, score: float, unlocked: bool):

    subject = "Your Mock Test Report – Dyslexia EmpowerHub"

    unlock_msg = (
        "Congratulations! You have unlocked the next level."
        if unlocked
        else "Keep practicing to unlock the next level."
    )

    text_body = f"""
Hello {username},

Your mock test has been completed.

Score: {score}%

{unlock_msg}

Your detailed report is attached as a PDF.

Keep practicing — every attempt builds confidence.

Dyslexia EmpowerHub
"""

    html_body = f"""
<html>
<body style="font-family:Arial, Helvetica, sans-serif; background:#f7f9fc; padding:20px;">

<div style="max-width:600px; margin:auto; background:white; padding:30px; border-radius:8px;">

<h2 style="color:#2c3e50;">Mock Test Report</h2>

<p>Hello <strong>{username}</strong>,</p>

<p>Your mock pronunciation test has been successfully completed.</p>

<div style="background:#f1f4f8; padding:15px; border-radius:6px; margin:20px 0;">
<strong>Final Score:</strong> {score}%
</div>

<p>{unlock_msg}</p>

<p>
Your detailed performance report is attached as a PDF file.
You can review your pronunciation insights and progress there.
</p>

<hr style="margin:25px 0;">

<p style="font-size:14px; color:#555;">
Keep practicing — every attempt strengthens your speech confidence.
</p>

<p style="font-size:12px; color:#888;">
Dyslexia EmpowerHub<br>
One sound at a time.
</p>

</div>

</body>
</html>
"""

    return subject, text_body, html_body