def build_mock_pdf(attempt, username: str, next_level_unlocked: bool):
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from io import BytesIO
    from datetime import datetime

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    story = []

    # 🎨 COLORS
    BG = colors.HexColor("#F8FAFC")
    CARD = colors.white
    BORDER = colors.HexColor("#E2E8F0")
    PRIMARY = colors.HexColor("#4F46E5")
    TEXT = colors.HexColor("#1E293B")
    SUB = colors.HexColor("#64748B")

    # 🎨 STYLES
    title = ParagraphStyle("title", fontSize=18, textColor=PRIMARY, spaceAfter=6)
    section = ParagraphStyle("section", fontSize=13, textColor=TEXT, spaceAfter=8)
    normal = ParagraphStyle("normal", fontSize=11, textColor=TEXT, leading=14)
    small = ParagraphStyle("small", fontSize=10, textColor=SUB, leading=13)

    # ---------------- HEADER ----------------
    header = Table(
        [[Paragraph("<b>Dyslexia EmpowerHub - Mock Performance Report</b>", title)]],
        colWidths=[500]
    )

    header.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BG),
        ("BOX", (0, 0), (-1, -1), 0, BG),
        ("PADDING", (0, 0), (-1, -1), 12),
    ]))

    story.append(header)
    story.append(Spacer(1, 12))

    # ---------------- PROFILE ----------------
    profile = Table([
        ["Name", username],
        ["User ID", str(attempt.user_id)],
        ["Level", str(attempt.level_id)],
        ["Status", attempt.status.capitalize()]
    ], colWidths=[120, 360])

    profile.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CARD),
        ("BOX", (0, 0), (-1, -1), 1, BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("PADDING", (0, 0), (-1, -1), 10),
    ]))

    story.append(Paragraph("Candidate Profile", section))
    story.append(profile)
    story.append(Spacer(1, 16))

    # ---------------- SCORE ----------------
    score = attempt.total_score or 0

    score_color = "#16A34A" if score >= 85 else "#F59E0B" if score >= 65 else "#DC2626"

    score_box = Table([
        [Paragraph(f"<b>Final Score:</b> <font color='{score_color}'>{score}%</font>", normal)],
        [Paragraph(f"<b>Verdict:</b> {attempt.verdict.replace('_',' ').title()}", normal)],
        [Paragraph(f"<b>Confidence:</b> {round(score/100,2)}", small)]
    ], colWidths=[500])

    score_box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CARD),
        ("BOX", (0, 0), (-1, -1), 1, BORDER),
        ("PADDING", (0, 0), (-1, -1), 12),
    ]))

    story.append(Paragraph("Performance Summary", section))
    story.append(score_box)
    story.append(Spacer(1, 16))

    # ---------------- WORD ANALYSIS ----------------
    story.append(Paragraph("Detailed Analysis", section))

    words = attempt.results.get("words", [])

    for w in words:
        color = "#16A34A" if w["score"] >= 80 else "#DC2626"

        word_block = []

        word_block.append(
            Paragraph(f"<b>{w['expected']}</b> → {w['recognized']}", normal)
        )

        word_block.append(
            Paragraph(f"Score: <font color='{color}'>{w['score']}%</font> ({w['verdict']})", small)
        )

        for f in w.get("feedback", [])[:2]:
            word_block.append(Paragraph(f"• {f}", small))

        card = Table([[word_block]], colWidths=[500])

        card.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), CARD),
            ("BOX", (0, 0), (-1, -1), 1, BORDER),
            ("PADDING", (0, 0), (-1, -1), 10),
        ]))

        story.append(card)
        story.append(Spacer(1, 10))

    # ---------------- INSIGHTS ----------------
    story.append(Paragraph("Insights", section))

    weak = [w for w in words if w["score"] < 65]
    strong = [w for w in words if w["score"] >= 85]

    insights_text = []
    if strong:
        insights_text.append(Paragraph(f"✔ Strong in {len(strong)} items", normal))
    if weak:
        insights_text.append(Paragraph(f"⚠ Needs improvement in {len(weak)} items", normal))

    insights_box = Table([[insights_text]], colWidths=[500])

    insights_box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BG),
        ("BOX", (0, 0), (-1, -1), 1, BORDER),
        ("PADDING", (0, 0), (-1, -1), 12),
    ]))

    story.append(insights_box)
    story.append(Spacer(1, 16))

    # ---------------- RECOMMENDATIONS ----------------
    story.append(Paragraph("Recommended Actions", section))

    recs = [
        "Practice slowly with clarity",
        "Repeat difficult sounds",
        "Focus on full phrases",
        "Retry after revision"
    ]

    rec_box = Table([[Paragraph(f"• {r}", normal)] for r in recs], colWidths=[500])

    rec_box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CARD),
        ("BOX", (0, 0), (-1, -1), 1, BORDER),
        ("PADDING", (0, 0), (-1, -1), 10),
    ]))

    story.append(rec_box)
    story.append(Spacer(1, 20))

    # ---------------- FOOTER ----------------
    story.append(Paragraph(
        "<i>Generated by Dyslexia EmpowerHub • One step at a time</i>",
        ParagraphStyle("footer", fontSize=9, textColor=SUB)
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer