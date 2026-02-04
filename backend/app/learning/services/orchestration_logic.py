# app/learning/services/orchestration_logic.py

from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.learning.models.word import Word
from app.learning.models.level_word import LevelWord

# Practice pipeline (UPLOAD + CONVERT ONLY)
from app.practice.routes.upload import upload_audio
from app.practice.services.audio_service import convert_to_wav
from app.practice.services.eval_service import evaluate_similarity

# Insights
from app.insights.schemas import FeedbackIn
from app.insights.services.feedback_service import generate_feedback
from app.insights.services.recommendations_service import recommend_next_step

# TTS
from app.learning.routes.tts import tts_word_handler


PROGRESS_THRESHOLD = 50
MASTERY_THRESHOLD = 80


async def run_learning_pipeline(
    *,
    user_id: int,
    level_id: int,
    word_id: int,
    pace_mode: str,
    pace_value: int | None,
    spoken: str,
    file: UploadFile,
):
    """
    🎯 FULL LEARNING ORCHESTRATION PIPELINE
    Browser-first STT, backend-only evaluation.
    """

    print("\n" + "=" * 70)
    print("🚀 LEARNING PIPELINE STARTED")
    print("=" * 70)
    print(f"👤 User ID   : {user_id}")
    print(f"📚 Level ID  : {level_id}")
    print(f"📝 Word ID   : {word_id}")
    print(f"🏃 Pace Mode : {pace_mode}")
    print(f"🎚 Pace Value: {pace_value}")
    print(f"🗣️ Spoken    : {spoken}")
    print(f"🎤 File Name : {file.filename}")
    print("-" * 70)

    db: Session = SessionLocal()

    try:
        # =====================================================
        # 1️⃣ WORD VALIDATION
        # =====================================================
        print("\n🔍 STEP 1: Validating word against level...")
        word = db.query(Word).filter(
            Word.id == word_id,
            Word.level_id == level_id
        ).first()

        if not word:
            print("❌ Word validation failed")
            raise HTTPException(status_code=404, detail="Word not found")

        expected = word.text
        print(f"✅ Word validated → '{expected}'")

        # =====================================================
        # 2️⃣ TTS INSTRUCTION (STATIC / RUNTIME / BROWSER)
        # =====================================================
        print("\n🔊 STEP 2: Preparing TTS instruction...")
        tts_instruction = tts_word_handler(
            db=db,
            word_id=word_id,
            pace_mode=pace_mode,
            pace_value=pace_value,
        )
        print("🎧 TTS instruction =", tts_instruction)

        # =====================================================
        # 3️⃣ AUDIO UPLOAD (FOR RECORD / FUTURE ANALYTICS)
        # =====================================================
        print("\n📥 STEP 3: Uploading learner audio...")
        uploaded = await upload_audio(file, user_id)
        file_id = uploaded.file_id
        print("✅ Upload successful")
        print(f"🆔 File ID → {file_id}")

        # =====================================================
        # 4️⃣ CONVERT TO WAV (OPTIONAL – KEPT FOR FUTURE)
        # =====================================================
        print("\n🎼 STEP 4: Converting audio → WAV...")
        wav_path = convert_to_wav(file_id, user_id)
        print(f"🎵 WAV file created at → {wav_path}")

        # =====================================================
        # 5️⃣ EVALUATION (BROWSER STT)
        # =====================================================
        print("\n📊 STEP 5: Evaluating pronunciation...")
        score, verdict = evaluate_similarity(expected, spoken)

        progress_this_attempt = score >= PROGRESS_THRESHOLD
        mastered_this_attempt = score >= MASTERY_THRESHOLD

        print(f"📈 Similarity Score → {score}")
        print(f"⚖️ Verdict         → {verdict}")
        print(f"➡️ Progressed?     → {progress_this_attempt}")
        print(f"🏆 Mastered now?   → {mastered_this_attempt}")

        # =====================================================
        # 6️⃣ FEEDBACK ENGINE
        # =====================================================
        print("\n💬 STEP 6: Generating learner feedback...")
        feedback_input = FeedbackIn(
            word=expected,
            spoken=spoken,
            similarity=score,
            attempts=1,
            pace=pace_mode,
        )
        feedback = generate_feedback(feedback_input)
        print("📝 Feedback generated")

        # =====================================================
        # 7️⃣ RECOMMENDATION ENGINE
        # =====================================================
        print("\n🧭 STEP 7: Generating next-step recommendation...")
        recommendation = recommend_next_step(feedback_input)
        print("📌 Recommendation generated")

        # =====================================================
        # 8️⃣ UPDATE LEARNING STATE
        # =====================================================
        print("\n📦 STEP 8: Updating learning progress in DB...")
        level_word = db.query(LevelWord).filter(
            LevelWord.user_id == user_id,
            LevelWord.word_id == word_id,
            LevelWord.level_id == level_id,
        ).first()

        if not level_word:
            print("🆕 Creating new LevelWord record")
            level_word = LevelWord(
                user_id=user_id,
                level_id=level_id,
                word_id=word_id,
                attempts=0,
                correct_attempts=0,
                mastery_score=0,
                highest_score=0,
                is_mastered=False,
            )
            db.add(level_word)

        level_word.attempts += 1

        if progress_this_attempt:
            level_word.correct_attempts += 1
            print("✅ Counted as a correct attempt")
        else:
            print("❌ Counted as incorrect attempt")

        level_word.mastery_score = round(
            level_word.correct_attempts / level_word.attempts, 2
        )

        if score > (level_word.highest_score or 0):
            print("🔥 New highest score achieved!")
            level_word.highest_score = score

        level_word.is_mastered = (
            (level_word.highest_score or 0) >= MASTERY_THRESHOLD
        )

        db.commit()

        mastery_overall = level_word.is_mastered
        highest_score = level_word.highest_score
        total_attempts = level_word.attempts

        print("💾 DB update committed successfully")

    finally:
        db.close()
        print("🔒 DB session closed")

    # =====================================================
    # 🔟 FINAL RESPONSE
    # =====================================================
    print("\n🎉 PIPELINE COMPLETE")
    print("=" * 70)

    return {
        "word_id": word_id,
        "expected": expected,
        "spoken": spoken,
        "similarity": score,
        "verdict": verdict,
        "progress_this_attempt": progress_this_attempt,
        "mastered_this_attempt": mastered_this_attempt,
        "highest_score": highest_score,
        "total_attempts": total_attempts,
        "mastery_overall": mastery_overall,
        "feedback": feedback,
        "recommendation": recommendation,
        "tts": tts_instruction,
    }
