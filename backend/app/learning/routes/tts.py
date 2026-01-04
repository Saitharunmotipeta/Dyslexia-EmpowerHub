# app/learning/routes/tts.py
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.learning.models.word import Word
from app.learning.services.tts_services import generate_tts_audio


def tts_word_handler(db: Session, word_id: int, pace: int):
    word = db.query(Word).filter(Word.id == word_id).first()

    if not word:
        raise HTTPException(status_code=404, detail="Word not found")

    url = generate_tts_audio(word.text, pace)

    return {
        "word_id": word.id,
        "audio_url": url,
        "pace": pace
    }
