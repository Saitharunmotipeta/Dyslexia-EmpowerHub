import logging
from fastapi import UploadFile, File, HTTPException

from app.practice.routes.upload import upload_audio
from app.practice.services.audio_service import convert_to_wav
from app.practice.services.stt_service import speech_to_text_from_wav
from app.practice.services.eval_service import evaluate_similarity
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

    print("🔊 STEP 0 — Generating TTS...")
    tts_res = tts_word_handler(SessionLocal(), word_id, pace)
    tts_url = tts_res.get("audio_url")
    print(f"🎵 TTS Ready → {tts_url}")

    # =========================
    # 1️⃣ SAVE USER AUDIO
    # =========================
    print("\n📥 STEP 1 — Uploading learner audio...")
    uploaded = await upload_audio(file)
    file_id = uploaded.file_id
    print(f"✔️ Upload complete")
    print(f"🆔 File ID = {file_id}")

    # =========================
    # 2️⃣ CONVERT TO WAV
    # =========================
    print("\n🎼 STEP 2 — Converting → WAV...")
    wav_path = convert_to_wav(file_id)
    print(f"✔️ Converted")
    print(f"🎧 WAV Path = {wav_path}")

    # =========================
    # 3️⃣ SPEECH TO TEXT
    # =========================
    print("\n🗣️ STEP 3 — Speech Recognition…")
    stt = speech_to_text_from_wav(wav_path)
    spoken = stt.get("text", "")
    print(f"🧠 Heard = '{spoken}'")

    # =========================
    # 4️⃣ FETCH EXPECTED WORD
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
        print("\n📖 STEP 4 — Expected Word Lookup…")
        print(f"📘 Expected = '{expected}'")

        # =========================
        # 5️⃣ EVALUATE SIMILARITY
        # =========================
        print("\n📊 STEP 5 — Evaluating Pronunciation…")
        score, verdict = evaluate_similarity(expected, spoken)

        mastered_now = score >= 80

        print(f"🎯 Match = {score}%")
        print(f"⚖️ Verdict = {verdict}")
        print(f"🏆 Mastered This Attempt = {mastered_now}")

        # =========================
        # 6️⃣ UPDATE OVERALL MASTERY
        # =========================
        print("\n🛠 STEP 6 — Updating Learning Progress…")

        level_word = db.query(LevelWord).filter(
            LevelWord.word_id == word_id
        ).first()

        if not level_word:
            level_word = LevelWord(
                word_id=word_id,
                attempts=0,
                correct_attempts=0,
                mastery_score=0,
                is_mastered=False
            )
            db.add(level_word)

        # count attempts (for analytics)
        level_word.attempts += 1
        if mastered_now:
            level_word.correct_attempts += 1

        # keep mastery score for insights (NOT used to gate mastery)
        level_word.mastery_score = (
            level_word.correct_attempts / level_word.attempts
        )

        # ⭐ NEW — track BEST ATTEMPT EVER
        if score > (level_word.highest_score or 0):
            level_word.highest_score = score

        # 🧠 mastery is PERMANENT once score ≥ 80 at least once
        if (level_word.highest_score or 0) >= 80:
            level_word.is_mastered = True


        db.commit()

        print(f"📈 Attempts = {level_word.attempts}")
        print(f"✅ Correct = {level_word.correct_attempts}")
        print(f"⭐ Mastery Score = {round(level_word.mastery_score, 2)}")
        print(f"🎓 Word Mastered Overall = {level_word.is_mastered}")

    finally:
        db.close()

    print("\n✨ FLOW COMPLETE — Returning Result 🎁\n")

    return {
        "word_id": word_id,
        "expected": expected,
        "spoken": spoken,
        "similarity": score,
        "verdict": verdict,
        "mastered_this_attempt": mastered_now,
        "mastery_overall": level_word.is_mastered
    }
