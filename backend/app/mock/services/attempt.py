from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.mock.models.attempt import MockAttempt
from app.mock.utils.unlock import is_mock_unlocked, generate_attempt_code
from app.mock.services.word import get_mock_words_for_level
from app.mock.services.mock_trend_service import analyze_mock_trend
from app.insights.services.confidence_engine import calculate_confidence_index
from app.insights.services.weakness_engine import generate_weakness_heatmap


# -------------------------------------------------
# START MOCK ATTEMPT
# -------------------------------------------------

def start_mock_attempt(
    db: Session,
    level_id: int,
    user_id: int,
):

    unlocked = is_mock_unlocked(
        db=db,
        user_id=user_id,
        level_id=level_id,
    )

    if not unlocked:
        raise HTTPException(
            status_code=403,
            detail="You're almost there! Complete a little more practice to unlock the mock test 💪"
        )

    REQUIRED_WORDS = 3

    words = get_mock_words_for_level(
        db=db,
        level_id=level_id,
        limit=REQUIRED_WORDS
    )

    if len(words) < REQUIRED_WORDS:
        raise HTTPException(
            status_code=400,
            detail="Not enough mock words available for this level."
        )

    # -----------------------------
    # Generate unique attempt id
    # -----------------------------

    public_attempt_id = generate_attempt_code()

    while db.query(MockAttempt).filter(
        MockAttempt.public_attempt_id == public_attempt_id
    ).first():
        public_attempt_id = generate_attempt_code()

    attempt = MockAttempt(
        user_id=user_id,
        level_id=level_id,
        public_attempt_id=public_attempt_id,
        status="started",
        results={"words": []},
    )

    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    return {
        "public_attempt_id": attempt.public_attempt_id,
        "words": words,
        "message": "Mock test started. Take your time and speak clearly 🌱"
    }


# -------------------------------------------------
# FINALIZE MOCK ATTEMPT
# -------------------------------------------------

def finalize_mock_attempt(
    db: Session,
    user_id: int,
    public_attempt_id: str
):

    attempt = db.query(MockAttempt).filter(
        MockAttempt.public_attempt_id == public_attempt_id,
        MockAttempt.user_id == user_id
    ).first()

    if not attempt:
        raise HTTPException(
            status_code=404,
            detail="Mock attempt not found."
        )

    if attempt.status == "completed":
        raise HTTPException(
            status_code=400,
            detail="This mock test has already been completed."
        )

    words = attempt.results.get("words", [])

    if not words:
        raise HTTPException(
            status_code=400,
            detail="No responses recorded. Please attempt the words before finishing."
        )

    # -----------------------------
    # SCORE CALCULATION
    # -----------------------------

    scores = [w.get("score", 0) for w in words]

    total_score = round(sum(scores) / len(scores), 2)

    # -----------------------------
    # VERDICT
    # -----------------------------

    verdict = (
        "excellent" if total_score >= 85 else
        "good_progress" if total_score >= 65 else
        "keep_practicing"
    )

    confidence = round(total_score / 100, 2)

    # -----------------------------
    # PERFORMANCE METRICS
    # -----------------------------

    metrics = {
        "average_score": total_score,
        "attempted_words": len(words),
        "accuracy": confidence,
        "highest_word_score": max(scores),
        "lowest_word_score": min(scores)
    }

    # -----------------------------
    # RECOMMENDATIONS
    # -----------------------------

    recommendations = []

    if total_score < 65:
        recommendations.append({
            "focus": "pronunciation clarity",
            "priority": "high"
        })

    if metrics["lowest_word_score"] < 60:
        recommendations.append({
            "focus": "slow articulation",
            "priority": "medium"
        })

    if not recommendations:
        recommendations.append({
            "focus": "fluency and rhythm",
            "priority": "low"
        })

    # -----------------------------
    # LEARNING TIPS
    # -----------------------------

    tips = [
        "Speak slowly and clearly.",
        "Pause briefly between syllables.",
        "Repeat the word once before recording."
    ]

    # -----------------------------
    # NEXT STEPS
    # -----------------------------

    next_steps = [
        "Redo practice for difficult words.",
        "Attempt the next level when you feel confident."
    ]

    # -----------------------------
    # WORD FEEDBACK
    # -----------------------------

    detailed_feedback = []

    for w in words:

        score = w.get("score", 0)

        if score >= 85:
            feedback = "Excellent pronunciation."

        elif score >= 65:
            feedback = "Nice attempt — very close."

        else:
            feedback = "Good effort. Try slowing down the pronunciation."

        detailed_feedback.append({
            "word_id": w.get("word_id"),
            "score": score,
            "feedback": feedback
        })

    # -----------------------------
    # TREND ANALYSIS
    # -----------------------------

    trend = analyze_mock_trend(
        db=db,
        user_id=user_id,
        level_id=attempt.level_id
    )

    # -----------------------------
    # UPDATE ATTEMPT
    # -----------------------------

    attempt.total_score = total_score
    attempt.verdict = verdict
    attempt.status = "completed"
    attempt.completed_at = datetime.utcnow()

    confidence_index = calculate_confidence_index(db, user_id)

    weakness_heatmap = generate_weakness_heatmap(db, user_id)

    db.commit()
    return {
        "public_attempt_id": attempt.public_attempt_id,
        "score": total_score,
        "verdict": verdict,
        "confidence": confidence,
        "confidence_index": confidence_index,
        "weakness_heatmap": weakness_heatmap,
        "trend": trend,
        "words": words,
        "message": _motivational_message(verdict),
        "metrics": metrics,
        "recommendations": recommendations,
        "tips": tips,
        "next_steps": next_steps,
        "detailed_feedback": detailed_feedback
    }


# -------------------------------------------------
# SUPPORTIVE MESSAGE
# -------------------------------------------------

def _motivational_message(verdict: str) -> str:

    messages = {
        "excellent": "Amazing work! Your pronunciation sounded confident and clear 🌟",
        "good_progress": "Great progress! With a little more practice you'll master it 💪",
        "keep_practicing": "Every attempt builds confidence. Keep practicing — you're learning 🧠"
    }

    return messages.get(verdict, "Nice effort! Keep going 🌱")