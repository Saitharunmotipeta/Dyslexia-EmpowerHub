# app/learning/services/orchestration_logic.py

from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.learning.models.word import Word
from app.learning.models.level_word import LevelWord

# Practice pipeline
from app.practice.routes.upload import upload_audio
from app.practice.services.audio_service import convert_to_wav
from app.practice.services.stt_service import speech_to_text_from_wav
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
    file: UploadFile,
):
    """
    🎯 FULL LEARNING ORCHESTRATION PIPELINE
    This is the SINGLE source of truth.
    """

    print("\n" + "=" * 70)
    print("🚀 LEARNING PIPELINE STARTED")
    print("=" * 70)
    print(f"👤 User ID   : {user_id}")
    print(f"📚 Level ID  : {level_id}")
    print(f"📝 Word ID   : {word_id}")
    print(f"🏃 Pace Mode : {pace_mode}")
    print(f"🎚 Pace Value: {pace_value}")
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
        # 2️⃣ TTS GENERATION / FETCH
        # =====================================================
        print("\n🔊 STEP 2: Generating / Fetching TTS audio...")
        tts_res = tts_word_handler(
            db,
            word_id,
            pace_mode,
            pace_value,
        )
        tts_url = tts_res.get("audio_url")
        print(f"🎧 TTS audio ready → {tts_url}")

        # =====================================================
        # 3️⃣ AUDIO UPLOAD
        # =====================================================
        print("\n📥 STEP 3: Uploading learner audio...")
        uploaded = await upload_audio(file, user_id)
        file_id = uploaded.file_id
        print("✅ Upload successful")
        print(f"🆔 File ID → {file_id}")

        # =====================================================
        # 4️⃣ CONVERT TO WAV
        # =====================================================
        print("\n🎼 STEP 4: Converting audio → WAV...")
        wav_path = convert_to_wav(file_id, user_id)
        print(f"🎵 WAV file created at → {wav_path}")

        # =====================================================
        # 5️⃣ SPEECH TO TEXT
        # =====================================================
        print("\n🗣️ STEP 5: Running Speech-to-Text (VOSK)...")
        stt_res = speech_to_text_from_wav(wav_path)
        spoken = stt_res.get("text", "").strip()
        print(f"🧠 Recognized Speech → '{spoken}'")

        # =====================================================
        # 6️⃣ EVALUATION
        # =====================================================
        print("\n📊 STEP 6: Evaluating pronunciation...")
        score, verdict = evaluate_similarity(expected, spoken)

        progress_this_attempt = score >= PROGRESS_THRESHOLD
        mastered_this_attempt = score >= MASTERY_THRESHOLD

        print(f"📈 Similarity Score → {score}")
        print(f"⚖️ Verdict         → {verdict}")
        print(f"➡️ Progressed?     → {progress_this_attempt}")
        print(f"🏆 Mastered now?   → {mastered_this_attempt}")

        # =====================================================
        # 7️⃣ FEEDBACK ENGINE
        # =====================================================
        print("\n💬 STEP 7: Generating learner feedback...")
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
        # 8️⃣ RECOMMENDATION ENGINE
        # =====================================================
        print("\n🧭 STEP 8: Generating next-step recommendation...")
        recommendation = recommend_next_step(feedback_input)
        print("📌 Recommendation generated")

        # =====================================================
        # 9️⃣ UPDATE LEARNING STATE (DB)
        # =====================================================
        print("\n📦 STEP 9: Updating learning progress in DB...")
        level_word = db.query(LevelWord).filter(
            LevelWord.user_id == user_id,
            LevelWord.word_id == word_id,
            LevelWord.level_id == level_id,
        ).first()

        if not level_word:
            print("🆕 No existing record — creating new LevelWord")
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

        "tts_audio": tts_url,
    }
