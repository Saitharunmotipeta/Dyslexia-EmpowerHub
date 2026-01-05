# app/learning/routes/learning_automation.py

import logging
from fastapi import UploadFile, File, HTTPException

from app.practice.routes.upload import upload_audio
from app.practice.services.audio_service import convert_to_wav
from app.practice.services.stt_service import speech_to_text_from_wav
from app.practice.services.eval_service import evaluate_similarity

# ⭐ Insights engines
from app.insights.services.feedback_service import generate_feedback
from app.insights.services.recommendations_service import recommend_next_step
from app.insights.schemas import FeedbackIn   # <-- IMPORTANT

from app.learning.routes.tts import tts_word_handler
from app.learning.models.word import Word
from app.learning.models.level_word import LevelWord
from app.database.connection import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("learning-automation")


async def learning_automation_handler(
    level_id: int,
    word_id: int,
    pace: int,
    file: UploadFile = File(...)
):

    print("\n🚀 LEARNING FLOW STARTED")
    print(f"📚 Level = {level_id}")
    print(f"📝 Word ID = {word_id}")
    print(f"⏩ Pace = {pace}")

    # =========================
    # 0️⃣ TTS
    # =========================
    print("🔊 STEP 0 — Generating TTS...")
    tts_res = tts_word_handler(SessionLocal(), word_id, pace)
    tts_url = tts_res.get("audio_url")
    print(f"🎵 TTS Ready → {tts_url}")

    # =========================
    # 1️⃣ UPLOAD
    # =========================
    print("\n📥 STEP 1 — Uploading learner audio...")
    uploaded = await upload_audio(file)
    file_id = uploaded.file_id
    print(f"🆔 File ID = {file_id}")

    # =========================
    # 2️⃣ CONVERT
    # =========================
    wav_path = convert_to_wav(file_id)
    print(f"🎧 WAV Path = {wav_path}")

    # =========================
    # 3️⃣ STT
    # =========================
    stt = speech_to_text_from_wav(wav_path)
    spoken = stt.get("text", "")
    print(f"🧠 Heard = '{spoken}'")

    # =========================
    # 4️⃣ DB: EXPECTED WORD
    # =========================
    db = SessionLocal()

    try:
        word = db.query(Word).filter(
            Word.id == word_id,
            Word.level_id == level_id
        ).first()

        if not word:
            raise HTTPException(404, "Word not found")

        expected = word.text
        print(f"📘 Expected = '{expected}'")

        # =========================
        # 5️⃣ EVALUATE
        # =========================
        score, verdict = evaluate_similarity(expected, spoken)

        mastered_now = score >= 80

        print(f"🎯 Match = {score}% ({verdict})")

        # =========================
        # 6️⃣ FEEDBACK ENGINE
        # =========================

        feedback_input = FeedbackIn(
            word=expected,
            spoken=spoken,
            similarity=score,
            attempts=1,
            pace="custom"
        )

        feedback = generate_feedback(feedback_input)
        print("\n💬 FEEDBACK →", feedback)

        # =========================
        # 7️⃣ RECOMMENDATION ENGINE
        # =========================

        recommendation = recommend_next_step(feedback_input)
        print("\n🧭 RECOMMENDATION →", recommendation)

        # =========================
        # 8️⃣ UPDATE DB
        # =========================
        level_word = db.query(LevelWord).filter(
            LevelWord.word_id == word_id
        ).first()

        if not level_word:
            level_word = LevelWord(
                word_id=word_id,
                attempts=0,
                correct_attempts=0,
                mastery_score=0,
                highest_score=0,
                is_mastered=False
            )
            db.add(level_word)

        level_word.attempts += 1
        if mastered_now:
            level_word.correct_attempts += 1

        # keep historical mastery_score for analytics
        level_word.mastery_score = (
            level_word.correct_attempts / level_word.attempts
        )

        # update highest score logic
        if score > (level_word.highest_score or 0):
            level_word.highest_score = score

        # only highest score decides mastery
        level_word.is_mastered = (level_word.highest_score or 0) >= 80

        db.commit()

        # ⭐⭐ CACHE VALUES BEFORE CLOSING SESSION ⭐⭐
        mastery_overall = level_word.is_mastered
        highest_score = level_word.highest_score
        total_attempts = level_word.attempts

    finally:
        db.close()

    print("\n✨ FLOW COMPLETE\n")

    return {
        "word_id": word_id,
        "expected": expected,
        "spoken": spoken,
        "similarity": score,
        "verdict": verdict,
        "mastered_this_attempt": mastered_now,
        "highest_score": highest_score,
        "total_attempts": total_attempts,
        "mastery_overall": mastery_overall,
        "feedback": feedback,
        "recommendation": recommendation
    }
