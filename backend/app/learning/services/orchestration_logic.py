# app/learning/services/orchestration_logic.py
import logging
import requests

from sqlalchemy.orm import Session
from app.learning.models.word import Word
from app.learning.models.level_word import LevelWord

API_BASE = "http://localhost:8000"

PACE_MAP = {
    "slow": 40,
    "medium": 80,
    "fast": 120
}

logging.basicConfig(level=logging.INFO)


def run_learning_pipeline(db: Session, user_id: int, level_id: int, word_id: int, pace: str):
    logging.info("🚀 Starting Learning Automation Pipeline")
    logging.info(f"👤 User={user_id}  🎯 Level={level_id}  📝 Word={word_id}  🏃 Pace={pace}")

    debug_log = {}

    # ===============================
    # 1️⃣ Fetch word for validation
    # ===============================
    word = db.query(Word).filter(
        Word.id == word_id,
        Word.level_id == level_id
    ).first()

    if not word:
        raise Exception("Word not found in this level")

    debug_log["word_text"] = word.text

    # ===============================
    # 2️⃣ Get TTS Audio
    # ===============================
    pace_val = PACE_MAP.get(pace, 80)

    logging.info(f"🎧 Generating TTS for '{word.text}' @ pace={pace_val}")

    tts_res = requests.get(
        f"{API_BASE}/learning/tts/{word_id}",
        params={"pace": pace_val}
    )

    audio_url = tts_res.json()["audio_url"]

    debug_log["tts_audio_url"] = audio_url

    # ===============================
    # 3️⃣ Upload practice audio (frontend will replace mp3 input)
    # ===============================
    logging.info("🎙 Uploading user audio")

    files = {"file": ("speech.mp3", open("sample_audio.mp3", "rb"))}
    upload_res = requests.post(f"{API_BASE}/practice/upload", files=files)

    file_id = upload_res.json()["file_id"]
    debug_log["file_id"] = file_id

    # ===============================
    # 4️⃣ Convert → WAV
    # ===============================
    logging.info("🔄 Converting audio → WAV...")
    requests.post(f"{API_BASE}/practice/convert/{file_id}")

    # ===============================
    # 5️⃣ STT — Recognize Speech
    # ===============================
    logging.info("🧠 Running STT")
    stt_res = requests.post(f"{API_BASE}/practice/stt/{file_id}")
    spoken_text = stt_res.json()["recognized_text"]

    debug_log["spoken_text"] = spoken_text

    # ===============================
    # 6️⃣ Evaluate
    # ===============================
    logging.info("📊 Evaluating similarity...")
    eval_res = requests.post(
        f"{API_BASE}/practice/evaluate",
        json={"expected_text": word.text, "spoken_text": spoken_text},
    )

    eval_json = eval_res.json()
    score = eval_json["similarity_percent"]

    debug_log["similarity_score"] = score

    mastered = score >= 70
    debug_log["is_mastered"] = mastered

    # ===============================
    # 7️⃣ Update DB status
    # ===============================
    logging.info("🟢 Updating DB learning progress...")

    requests.post(
        f"{API_BASE}/learning/words/{word_id}/update_status",
        params={"is_mastered": mastered, "mastery_score": score},
        headers={"Authorization": f"Bearer {user_id}"}
    )

    # ===============================
    # 8️⃣ Return analytics
    # ===============================
    logging.info("✨ Pipeline complete")

    return debug_log
