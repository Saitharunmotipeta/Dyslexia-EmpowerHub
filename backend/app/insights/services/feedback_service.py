from app.insights.schemas import FeedbackIn, FeedbackOut
from fastapi import Depends
from app.database.connection import get_db
from app.auth.dependencies import get_current_user_id
from app.insights.services.trends import trend_analysis
from app.insights.services.pattern_service import detect_error_pattern
from app.insights.services.rag_service import generate_reasoning
from app.insights.services.weakness_engine import generate_weakness_heatmap
from sqlalchemy.orm import Session


# 🔥 RESPONSE CLEANER (DYSLEXIA FRIENDLY)
def clean_response(text: str) -> str:
    if not text:
        return ""

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    filtered = []
    for line in lines:
        if "let's fix" in line.lower():
            continue
        filtered.append(line)

    clean_lines = []
    for line in filtered[:2]:
        words = line.split()[:30]
        clean_lines.append(" ".join(words))

    return "\n".join(clean_lines)


def is_bad_response(text: str) -> bool:
    if not text:
        return True

    bad_keywords = ["spell", "letter", "typed", "spelling"]
    return any(word in text.lower() for word in bad_keywords)


# 🔥 UPDATED: ADD alignment
def generate_feedback(
    data: FeedbackIn,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
    alignment=None   # 🔥 NEW
) -> FeedbackOut:

    score = data.score
    attempts = data.attempts
    content_type = data.content_type

    trend = trend_analysis(score, attempts, recent_scores=None)

    pattern = detect_error_pattern(
        expected=data.text,
        spoken=data.spoken,
        content_type=content_type,
        alignment=alignment   # 🔥 NEW
    )

    feedback_msgs = []

    # -------------------------
    # Verdict (UNCHANGED)
    # -------------------------

    if score >= 90:
        verdict = "excellent"
        feedback_msgs.append("Clear and confident — beautifully spoken 🌟")

    elif score >= 75:
        verdict = "good"
        feedback_msgs.append("You're very close — small adjustments will make it perfect 🔥")

    elif score >= 55:
        verdict = "improving"
        feedback_msgs.append("You’re building fluency. Keep practicing slowly 💪")

    else:
        verdict = "needs_practice"
        feedback_msgs.append("Take your time. Break it into parts and try again 🧠")

    # -------------------------
    # 🔥 NEW: ALIGNMENT-BASED FEEDBACK (CORE FIX)
    # -------------------------

    mistakes = []

    if alignment:
        for item in alignment:
            if item["type"] == "substitution":
                if item.get("expected") and item.get("spoken"):
                    feedback_msgs.append(
                        f"You said '{item['spoken']}' instead of '{item['expected']}'"
                    )
                    mistakes.append(item["expected"])

            elif item["type"] == "missing":
                feedback_msgs.append(
                    f"You missed the word '{item['expected']}'"
                )
                mistakes.append(item["expected"])

            elif item["type"] == "extra":
                feedback_msgs.append(
                    f"You added an extra word '{item['spoken']}'"
                )

        # 🔥 Add summary line
        if mistakes:
            feedback_msgs.append("Focus on correcting specific words.")

    # -------------------------
    # 🔥 OPTIONAL AI REASONING (SECONDARY)
    # -------------------------

    if pattern and pattern.get("code") not in ["normal", "correct"]:

        try:
            rag_explanation = generate_reasoning(
                expected=data.text,
                spoken=data.spoken,
                pattern=pattern
            )

            rag_explanation = clean_response(rag_explanation)

            if not is_bad_response(rag_explanation):
                feedback_msgs.append(rag_explanation)

        except Exception:
            pass  # safe ignore

    # -------------------------
    # TREND
    # -------------------------

    if trend:
        feedback_msgs.append(clean_response(trend["message"]))
        feedback_msgs.append(clean_response(trend["tip"]))

    # -------------------------
    # REMOVE DUPLICATES
    # -------------------------

    feedback_msgs = list(dict.fromkeys(feedback_msgs))

    # -------------------------
    # WEAKNESS HEATMAP
    # -------------------------

    weakness_data = generate_weakness_heatmap(db, user_id)

    if weakness_data["message"]:
        feedback_msgs.append(weakness_data["message"])

    # -------------------------
    # Confidence Tip
    # -------------------------

    confidence_tip = (
        "Progress builds with repetition. Speak slowly. Stay consistent 💙"
    )

    return FeedbackOut(
        verdict=verdict,
        score=round(score, 2),
        feedback=feedback_msgs,
        confidence_tip=confidence_tip
    )