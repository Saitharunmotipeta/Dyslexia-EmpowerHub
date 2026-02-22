from sqlalchemy.orm import Session
from sqlalchemy import asc
import re

from app.learning.models.word import Word
from app.learning.models.level import Level


def extract_numbers(message: str):
    numbers = re.findall(r"\d+", message)
    if len(numbers) >= 2:
        return int(numbers[0]), int(numbers[1])
    return None, None


def run(user_id: int, db: Session, message: str = None) -> dict | None:

    level_order, word_position = extract_numbers(message)

    if not level_order or not word_position:
        return {"error": "invalid_query"}

    level = (
        db.query(Level)
        .filter(Level.order == level_order)
        .first()
    )

    if not level:
        return {"error": "level_not_found"}

    words = (
        db.query(Word)
        .filter(Word.level_id == level.id)
        .order_by(asc(Word.id))
        .all()
    )

    if word_position > len(words):
        return {"error": "word_not_found"}

    target_word = words[word_position - 1]

    return {
        "level_name": level.name,
        "word_text": target_word.text,
        "phonetics": target_word.phonetics,
        "syllables": target_word.syllables,
        "syllable_count": target_word.syllable_count,
        "difficulty": target_word.difficulty,
    }