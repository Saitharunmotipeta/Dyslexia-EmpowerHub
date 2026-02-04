from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.learning.models.word import Word
from app.learning.models.level_word import LevelWord
from app.database.connection import SessionLocal

from app.practice.services.eval_service import evaluate_similarity

from app.insights.schemas import FeedbackIn
from app.insights.services.feedback_service import generate_feedback
from app.insights.services.recommendations_service import recommend_next_step


async def run_practice_flow(
    *,
    word_id: int,
    level_id: int,
    spoken: str,
    user_id: int,
):
    """
    Browser-based practice orchestration.
    """

    spoken = spoken.strip().lower()

    if not spoken:
        raise HTTPException(
            status_code=400,
            detail="Spoken text cannot be empty",
        )

    print("\n🚀 PRACTICE FLOW STARTED")
    print(f"🆔 user_id = {user_id}")
    print(f"🆔 word_id = {word_id}")
    print(f"🗣 spoken = '{spoken}'")

    db: Session = SessionLocal()

    try:
        # -------------------------
        # 1️⃣ Fetch expected word
        # -------------------------
        print("\n📚 Fetching expected word...")
        word = db.query(Word).filter(Word.id == word_id).first()
        if not word:
            raise HTTPException(status_code=404, detail="Word not found")

        expected = word.text.lower()
        print(f"📖 Expected = '{expected}'")

        # -------------------------
        # 2️⃣ Evaluate similarity
        # -------------------------
        print("\n📊 Evaluating pronunciation...")
        similarity_percent, verdict = evaluate_similarity(expected, spoken)

        print(f"🧪 Similarity = {similarity_percent}%")
        print(f"⚖️ Verdict = {verdict}")

        # -------------------------
        # 3️⃣ Update learning progress
        # -------------------------
        print("\n📈 Updating progress...")

        level_word = (
            db.query(LevelWord)
            .filter(
                LevelWord.user_id == user_id,
                LevelWord.word_id == word_id,
                LevelWord.level_id == level_id,
            )
            .first()
        )

        if not level_word:
            print("🆕 Creating LevelWord record")
            level_word = LevelWord(
                user_id=user_id,
                word_id=word_id,
                level_id=level_id,
                attempts=0,
                correct_attempts=0,
                mastery_score=0.0,
                highest_score=0.0,
                is_mastered=False,
            )
            db.add(level_word)

        level_word.attempts += 1

        if similarity_percent >= 80:
            level_word.correct_attempts += 1
            print("🎯 Correct attempt")
        else:
            print("❌ Incorrect attempt")

        level_word.mastery_score = (
            level_word.correct_attempts / level_word.attempts
        )

        if similarity_percent > (level_word.highest_score or 0):
            level_word.highest_score = similarity_percent

        level_word.is_mastered = level_word.highest_score >= 80

        db.commit()

        attempts = level_word.attempts
        highest_score = level_word.highest_score
        is_mastered = level_word.is_mastered

    finally:
        db.close()

    # -------------------------
    # 4️⃣ Feedback + Recommendation
    # -------------------------
    feedback_input = FeedbackIn(
        word=expected,
        spoken=spoken,
        similarity=similarity_percent,
        attempts=attempts,
        pace="browser",
    )

    print("\n💬 Generating feedback...")
    feedback = generate_feedback(feedback_input)

    print("\n🧭 Generating recommendation...")
    recommendation = recommend_next_step(feedback_input)

    # -------------------------
    # 5️⃣ Final response
    # -------------------------
    print("\n🎉 PRACTICE FLOW COMPLETE\n")

    return {
        "word_id": word_id,
        "expected": expected,
        "spoken": spoken,
        "similarity": similarity_percent,
        "verdict": verdict,
        "is_mastered": is_mastered,
        "attempts": attempts,
        "highest_score": highest_score,
        "feedback": feedback,
        "recommendation": recommendation,
    }
