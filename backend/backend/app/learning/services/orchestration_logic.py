# app/learning/services/orchestration_logic.py

import logging
import requests

from app.insights.schemas import FeedbackIn
from app.insights.services.feedback_service import generate_feedback
from app.insights.services.recommendations_service import recommend_next_step

from app.learning.models.word import Word
from app.learning.models.level_word import LevelWord
from app.database.connection import SessionLocal

API_BASE = "http://localhost:8000"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("orchestration")


def run_learning_pipeline(user_id: int, level_id: int, word_id: int, pace: int = 80):

    print("\n🚀 ORCHESTRATION STARTED")
    print(f"📚 Level = {level_id}")
    print(f"📝 Word ID = {word_id}")
    print(f"🏃 Pace = {pace}")

    db = SessionLocal()

    try:
        # 1️⃣ Validate Word
        word = db.query(Word).filter(
            Word.id == word_id,
            Word.level_id == level_id
        ).first()

        if not word:
            raise Exception("Word not found for level")

        expected = word.text

        # 2️⃣ Get TTS
        print("\n🔊 Fetching TTS audio…")
        tts = requests.get(f"{API_BASE}/learning/tts/{word_id}", params={"pace": pace})
        tts_url = tts.json()["audio_url"]
        print(f"🎵 TTS Ready → {tts_url}")

        # 3️⃣ Upload sample file (frontend later replaces)
        print("\n📥 Uploading learner audio…")
        files = {"file": ("speech.mp3", open("sample_audio.mp3", "rb"))}
        upload = requests.post(f"{API_BASE}/practice/upload", files=files)
        file_id = upload.json()["file_id"]

        # 4️⃣ Convert
        print("\n🎼 Converting → WAV…")
        requests.post(f"{API_BASE}/practice/convert/{file_id}")

        # 5️⃣ STT
        print("\n🗣️ Running STT…")
        stt = requests.post(f"{API_BASE}/practice/stt/{file_id}").json()
        spoken = stt["recognized_text"]

        # 6️⃣ Evaluate
        print("\n📊 Evaluating similarity…")
        eval_res = requests.post(
            f"{API_BASE}/practice/evaluate",
            json={"expected_text": expected, "spoken_text": spoken}
        ).json()

        score = eval_res["similarity_percent"]
        verdict = eval_res["verdict"]

        mastered_now = score >= 80

        # 7️⃣ Feedback + Recommendation
        feedback_input = FeedbackIn(
            word=expected,
            spoken=spoken,
            similarity=score,
            attempts=1,
            pace="custom"
        )

        feedback = generate_feedback(feedback_input)
        recommendation = recommend_next_step(feedback_input)

        # 8️⃣ Update learning record
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

        # historical stat only
        level_word.mastery_score = (
            level_word.correct_attempts / level_word.attempts
        )

        # highest score logic
        if score > (level_word.highest_score or 0):
            level_word.highest_score = score

        level_word.is_mastered = (level_word.highest_score or 0) >= 80

        db.commit()

        mastery_overall = level_word.is_mastered
        highest_score = level_word.highest_score
        total_attempts = level_word.attempts

    finally:
        db.close()

    print("\n✨ ORCHESTRATION COMPLETE")

    return {
        "expected": expected,
        "spoken": spoken,
        "similarity": score,
        "verdict": verdict,
        "highest_score": highest_score,
        "total_attempts": total_attempts,
        "mastery_overall": mastery_overall,
        "feedback": feedback,
        "recommendation": recommendation
    }
