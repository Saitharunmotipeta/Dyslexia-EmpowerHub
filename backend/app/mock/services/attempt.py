from datetime import datetime
from sqlalchemy.orm import Session

from app.mock.models.attempt import MockAttempt
from app.mock.utils.unlock import is_mock_unlocked
from app.mock.services.word import get_mock_words_for_level


# -------------------------------
# START MOCK ATTEMPT
# -------------------------------

def start_mock_attempt(
    db: Session,
    user_id: int,
    level_id: int
):
    """
    1. Check unlock rule
    2. Pick 3 words
    3. Create mock attempt
    """

    # 1️⃣ Unlock check
    unlocked = is_mock_unlocked(
        db=db,
        user_id=user_id,
        level_id=level_id
    )

    if not unlocked:
        raise PermissionError(
            "You’re almost there! Complete more practice to unlock the mock test 💪"
        )

    # 2️⃣ Pick words (exactly 3)
    words = get_mock_words_for_level(
        db=db,
        level_id=level_id,
        limit=3
    )

    if len(words) < 3:
        raise ValueError("Not enough words available for this level")

    # 3️⃣ Create attempt
    attempt = MockAttempt(
        user_id=user_id,
        level_id=level_id,
        status="started",
        results={"words": []}
    )

    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    return {
        "attempt_id": attempt.id,
        "level_id": level_id,
        "words": words,
        "message": "Mock test started. Take your time — you’ve got this 🌱"
    }


# -------------------------------
# FINALIZE MOCK ATTEMPT
# -------------------------------

def finalize_mock_attempt(
    db: Session,
    user_id: int,
    attempt_id: int
):
    attempt = db.query(MockAttempt).filter(
        MockAttempt.id == attempt_id,
        MockAttempt.user_id == user_id
    ).first()

    if not attempt:
        raise ValueError("Mock attempt not found")

    words = attempt.results.get("words", [])

    if not words:
        raise ValueError("No words attempted")

    scores = [w.get("score", 0) for w in words]
    total_score = round(sum(scores) / len(scores), 2)

    verdict = (
        "excellent" if total_score >= 85 else
        "good_progress" if total_score >= 65 else
        "keep_practicing"
    )

    confidence = round(total_score / 100, 2)

    metrics = {
        "average_score": total_score,
        "attempted_words": len(words),
        "accuracy": confidence
    }

    recommendations = [
        {"focus": "pronunciation", "priority": "medium"}
        if verdict != "excellent"
        else {"focus": "fluency", "priority": "low"}
    ]

    tips = [
        "Speak slowly and clearly",
        "Repeat the word once before recording"
    ]

    next_steps = [
        "Redo practice for weak words",
        "Attempt next level when ready"
    ]

    detailed_feedback = [
        {
            "word_id": w["word_id"],
            "feedback": "Good attempt, minor pronunciation issue"
            if w["score"] < 85 else "Well pronounced"
        }
        for w in words
    ]

    attempt.total_score = total_score
    attempt.verdict = verdict
    attempt.status = "completed"
    attempt.completed_at = datetime.utcnow()

    db.commit()

    # ✅ SCHEMA-COMPLIANT RESPONSE
    return {
        "attempt_id": attempt.id,
        "score": total_score,
        "verdict": verdict,
        "words": words,
        "message": _motivational_message(verdict),
        "recommendations": recommendations,
        "confidence": confidence,
        "metrics": metrics,
        "tips": tips,
        "next_steps": next_steps,
        "detailed_feedback": detailed_feedback
    }

# -------------------------------
# SUPPORTIVE MESSAGE
# -------------------------------

def _motivational_message(verdict: str) -> str:
    return {
        "excellent": "Amazing work! Your effort is paying off 🌟",
        "good_progress": "Great progress! A little more practice and you’ll nail it 💪",
        "keep_practicing": "Every attempt makes you stronger. Keep going — you’re learning 🧠"
    }.get(verdict, "Nice work! Keep practicing 🌱")
