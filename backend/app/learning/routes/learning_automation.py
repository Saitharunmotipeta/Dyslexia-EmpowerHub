# app/learning/routes/learning_automation.py

import logging
from fastapi import UploadFile, File, HTTPException

from app.practice.routes.upload import upload_audio
from app.practice.services.audio_service import convert_to_wav
from app.practice.services.stt_service import speech_to_text_from_wav
from app.practice.services.eval_service import evaluate_similarity

# Insights engines
from app.insights.services.feedback_service import generate_feedback
from app.insights.services.recommendations_service import recommend_next_step
from app.insights.schemas import FeedbackIn

from app.learning.routes.tts import tts_word_handler
from app.learning.models.word import Word
from app.learning.models.level_word import LevelWord
from app.database.connection import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("learning-automation")

# -------------------------------
# CONFIG (single source of truth)
# -------------------------------

PROGRESS_THRESHOLD = 50        # learner is moving forward
MASTERY_THRESHOLD = 80         # learner has mastered the word


async def learning_automation_handler(
    level_id: int,
    word_id: int,
    user_id: int,
    pace: int,
    file: UploadFile = File(...)
):
    print("🚀 Learning automation started")

    # =========================
    # 0️⃣ TTS
    # =========================
    tts_res = tts_word_handler(SessionLocal(), word_id, pace)
    db = SessionLocal()
    try:
        tts_res = tts_word_handler(db, word_id, pace)
    finally:
        db.close()
    tts_url = tts_res.get("audio_url")

    # =========================
    # 1️⃣ UPLOAD
    # =========================
    uploaded = await upload_audio(file, user_id)
    file_id = uploaded.file_id

    # =========================
    # 2️⃣ CONVERT
    # =========================
    wav_path = convert_to_wav(file_id, user_id)

    # =========================
    # 3️⃣ STT
    # =========================
    stt = speech_to_text_from_wav(wav_path)
    spoken = stt.get("text", "").strip()

    # =========================
    # 4️⃣ DB LOOKUP
    # =========================
    db = SessionLocal()

    try:
        word = db.query(Word).filter(
            Word.id == word_id,
            Word.level_id == level_id
        ).first()

        if not word:
            raise HTTPException(status_code=404, detail="Word not found")

        expected = word.text

        # =========================
        # 5️⃣ EVALUATION
        # =========================
        score, verdict = evaluate_similarity(expected, spoken)

        # Progress ≠ Mastery (THIS IS THE FIX)
        progress_this_attempt = score >= PROGRESS_THRESHOLD
        mastered_this_attempt = score >= MASTERY_THRESHOLD

        # =========================
        # 6️⃣ FEEDBACK ENGINE
        # =========================
        feedback_input = FeedbackIn(
            word=expected,
            spoken=spoken,
            similarity=score,
            attempts=1,          # single-shot context
            pace="custom"
        )

        feedback = generate_feedback(feedback_input)

        # =========================
        # 7️⃣ RECOMMENDATION ENGINE
        # =========================
        recommendation = recommend_next_step(feedback_input)

        # =========================
        # 8️⃣ UPDATE LEARNING STATE
        # =========================
        level_word = db.query(LevelWord).filter(
            LevelWord.user_id == user_id,
            LevelWord.word_id == word_id,
            LevelWord.level_id == level_id
        ).first()

        if not level_word:
            level_word = LevelWord(
                user_id=user_id,            # optional / system driven
                level_id=level_id,
                word_id=word_id,
                attempts=0,
                correct_attempts=0,
                mastery_score=0,
                highest_score=0,
                is_mastered=False
            )
            db.add(level_word)

        # attempt tracking
        level_word.attempts += 1

        if progress_this_attempt:
            level_word.correct_attempts += 1

        # progress ratio (analytics only)
        level_word.mastery_score = round(
            level_word.correct_attempts / level_word.attempts,
            2
        )

        # highest score decides mastery (corporate-safe)
        if score > (level_word.highest_score or 0):
            level_word.highest_score = score

        level_word.is_mastered = (
            (level_word.highest_score or 0) >= MASTERY_THRESHOLD
        )

        db.commit()

        # cache before closing session
        mastery_overall = level_word.is_mastered
        highest_score = level_word.highest_score
        total_attempts = level_word.attempts

    finally:
        db.close()

    print("✅ Learning automation completed")

    # =========================
    # 9️⃣ RESPONSE CONTRACT
    # =========================
    return {
        "word_id": word_id,
        "expected": expected,
        "spoken": spoken,
        "similarity": score,
        "verdict": verdict,

        # 🔑 separated signals
        "progress_this_attempt": progress_this_attempt,
        "mastered_this_attempt": mastered_this_attempt,

        # 📊 historical metrics
        "highest_score": highest_score,
        "total_attempts": total_attempts,
        "mastery_overall": mastery_overall,

        # 🧠 insights
        "feedback": feedback,
        "recommendation": recommendation,

        # 🎧 extras (non-breaking)
        "tts_audio": tts_url
    }
