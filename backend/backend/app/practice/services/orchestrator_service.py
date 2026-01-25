# app/practice/services/orchestrator_service.py

import uuid
from fastapi import UploadFile, HTTPException

from app.practice.routes.upload import upload_audio
from app.practice.services.audio_service import convert_to_wav
from app.practice.services.stt_service import speech_to_text_from_wav
from app.practice.services.eval_service import evaluate_similarity

from app.learning.models.word import Word
from app.learning.models.level_word import LevelWord
from app.database.connection import SessionLocal

# ⭐ NEW — Insights Engine
from app.insights.schemas import FeedbackIn
from app.insights.services.feedback_service import generate_feedback
from app.insights.services.recommendations_service import recommend_next_step


async def run_practice_flow(word_id: int, file: UploadFile):
    """
    Orchestrates the full practice workflow.
    """

    file_id = str(uuid.uuid4())
    print("\n🚀 PRACTICE FLOW STARTED")
    print(f"🆔 word_id = {word_id}")
    print(f"🎵 incoming file = {file.filename}")
    print(f"🧾 generated file_id = {file_id}")

    # -------------------------
    # 1️⃣ Save Uploaded File
    # -------------------------
    print("\n📥 STEP 1: Uploading file...")
    uploaded = await upload_audio(file)
    uploaded_path = uploaded.file_id if hasattr(uploaded, "file_id") else uploaded
    print(f"✅ Upload done!")
    print(f"📂 Saved file reference = {uploaded_path}")

    # -------------------------
    # 2️⃣ Convert → WAV
    # -------------------------
    print("\n🎼 STEP 2: Converting to WAV...")
    wav_path = convert_to_wav(uploaded_path)
    print(f"✅ Conversion done!")
    print(f"🎧 WAV file path = {wav_path}")

    # -------------------------
    # 3️⃣ Speech-To-Text
    # -------------------------
    print("\n🗣️ STEP 3: Running VOSK STT...")
    stt_result = speech_to_text_from_wav(wav_path)
    spoken = stt_result.get("text", "")
    print(f"🧠 Recognized text = '{spoken}'")

    # -------------------------
    # 4️⃣ Fetch expected word
    # -------------------------
    print("\n📚 STEP 4: Fetching expected word from DB...")
    db = SessionLocal()
    try:
        word = db.query(Word).filter(Word.id == word_id).first()

        if not word:
            print("❌ Word not found in DB")
            raise HTTPException(status_code=404, detail="Word not found")

        expected = word.text
        print(f"📖 Expected word = '{expected}'")

        # -------------------------
        # 5️⃣ Evaluate similarity
        # -------------------------
        print("\n📊 STEP 5: Comparing spoken vs expected...")
        print(f"🔹 expected='{expected}'")
        print(f"🔹 spoken='{spoken}'")

        similarity_percent, verdict = evaluate_similarity(expected, spoken)

        print(f"🧪 Similarity score = {similarity_percent}%")
        print(f"⚖️ Verdict = {verdict}")

        # -------------------------
        # 6️⃣ Update Learning Progress
        # -------------------------
        print("\n📈 STEP 6: Updating learning progress...")

        level_word = (
            db.query(LevelWord)
            .filter(LevelWord.word_id == word_id)
            .first()
        )

        if not level_word:
            print("🆕 No record found — creating new LevelWord entry")
            level_word = LevelWord(
                word_id=word_id,
                attempts=0,
                correct_attempts=0,
                mastery_score=0,
                is_mastered=False,
                highest_score=0
            )
            db.add(level_word)

        level_word.attempts += 1

        # Track correctness historically (optional analytics)
        if similarity_percent >= 80:
            level_word.correct_attempts += 1
            print("🎯 Counted as CORRECT attempt")
        else:
            print("❌ Counted as INCORRECT attempt")

        # Historical ratio (for dashboards later)
        level_word.mastery_score = (
            level_word.correct_attempts / level_word.attempts
        )

        # 🚀 NEW — Highest score ever matters
        if similarity_percent > (level_word.highest_score or 0):
            level_word.highest_score = similarity_percent

        # Mastered flag = EVER got >= 80
        level_word.is_mastered = (level_word.highest_score or 0) >= 80

        db.commit()

        print(f"📊 Attempts = {level_word.attempts}")
        print(f"🏆 Correct Attempts = {level_word.correct_attempts}")
        print(f"⭐ Mastery Score = {round(level_word.mastery_score, 2)}")
        print(f"🔥 Highest Score = {level_word.highest_score}")
        print(f"🟢 Mastered? {level_word.is_mastered}")

    finally:
        db.close()

    # -------------------------
    # ⭐ 7️⃣ FEEDBACK + RECOMMENDATION
    # -------------------------

    feedback_input = FeedbackIn(
        word=expected,
        spoken=spoken,
        similarity=similarity_percent,
        attempts=level_word.attempts,
        pace="custom"
    )

    print("\n💬 Generating Feedback...")
    feedback = generate_feedback(feedback_input)
    print("📝 Feedback =", feedback)

    print("\n🧭 Generating Recommendation...")
    recommendation = recommend_next_step(feedback_input)
    print("📌 Recommendation =", recommendation)

    # -------------------------
    # 8️⃣ Return clean response
    # -------------------------
    print("\n🎉 STEP 8: Flow complete — sending response!\n")

    return {
        "file_id": file_id,
        "word_id": word_id,
        "expected": expected,
        "spoken": spoken,
        "similarity": similarity_percent,
        "verdict": verdict,
        "is_mastered": level_word.is_mastered,
        "attempts": level_word.attempts,
        "highest_score": level_word.highest_score,
        "feedback": feedback,
        "recommendation": recommendation
    }
