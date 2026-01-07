from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.mock.models.attempt import MockAttempt
from app.mock.utils.unlock import is_mock_unlocked
from app.mock.services.word import get_mock_words_for_level
from app.mock.utils.unlock import generate_attempt_code


# -------------------------------
# START MOCK ATTEMPT
# -------------------------------

def start_mock_attempt(
    db: Session,
    level_id: int,
    user_id: int,
):
    unlocked = is_mock_unlocked(
        db=db,
        user_id=user_id,
        level_id=level_id
    )

    if not unlocked:
        raise HTTPException(
            status_code=403,
            detail="You’re almost there! Complete more practice to unlock the mock test 💪"
        )
    REQUIRED_WORDS = 3

    # 1️⃣ Get random words (no unlock, no levels)
    words = get_mock_words_for_level(
        db=db,
        level_id=level_id,   # ✅ ADD THIS
        limit=REQUIRED_WORDS
    )


    if len(words) < REQUIRED_WORDS:
        raise HTTPException(
            status_code=400,
            detail="Not enough words available to start mock test"
        )

    # 2️⃣ Generate unique 6-digit attempt code
    attempt_code = generate_attempt_code()

    # (optional but safe uniqueness check)
    while db.query(MockAttempt).filter(
        MockAttempt.attempt_code == attempt_code
    ).first():
        attempt_code = generate_attempt_code()

    # 3️⃣ Create attempt
    attempt = MockAttempt(
        user_id=user_id,
        level_id=level_id,
        attempt_code=attempt_code,
        status="started",
        results={"words": []},
        started_at=datetime.utcnow()
    )

    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    return {
        "attempt_id": attempt.attempt_code,  # 🔑 public-facing
        "words": words,
        "message": "Mock test started. Take your time — you’ve got this 🌱"
    }
# -------------------------------
# FINALIZE MOCK ATTEMPT
# -------------------------------

def finalize_mock_attempt(
    db: Session,
    user_id: int,
    attempt_code: int
):
    attempt = db.query(MockAttempt).filter(
        MockAttempt.attempt_code == attempt_code,
        MockAttempt.user_id == user_id
    ).first()

    if not attempt:
        raise HTTPException(
            status_code=404,
            detail="Mock attempt not found"
        )

    # if attempt.status == "completed":
    #     raise HTTPException(
    #         status_code=400,
    #         detail="Mock test already completed"
    #     )

    attempt.status = "completed"
    attempt.completed_at = datetime.utcnow()
    # attempt.results["words"].append(word_result)
    # db.commit()
    words = attempt.results.get("words", [])

    # if not words:
    #     raise HTTPException(
    #         status_code=400,
    #         detail="No words attempted yet. Submit at least one word before viewing results."
    #     )

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
            "feedback": (
                "Well pronounced"
                if w.get("score", 0) >= 85
                else "Good attempt, minor pronunciation issue"
            )
        }
        for w in words
    ]

    attempt.total_score = total_score
    attempt.verdict = verdict
    attempt.status = "completed"
    attempt.completed_at = datetime.utcnow()

    db.commit()

    return {
        "attempt_id": attempt.attempt_code,  # ✅ public-safe
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
