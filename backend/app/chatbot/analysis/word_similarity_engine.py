from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.learning.models.level_word import LevelWord


def run(user_id: int, db: Session) -> dict | None:

    records = (
        db.query(LevelWord)
        .filter(LevelWord.user_id == user_id)
        .order_by(desc(LevelWord.last_practiced_at))
        .limit(50)
        .all()
    )

    if not records:
        return None

    similarity_values = []
    weak_words = []

    for r in records:
        similarity = r.last_similarity or 0
        similarity_values.append(similarity)

        if similarity < 50 and r.word:
            weak_words.append(r.word.text)

    avg_similarity = round(sum(similarity_values) / len(similarity_values), 2)

    dominant_weak_word = None
    if weak_words:
        dominant_weak_word = max(set(weak_words), key=weak_words.count)

    return {
        "records_checked": len(records),
        "average_similarity": avg_similarity,
        "above_50_count": len([s for s in similarity_values if s >= 50]),
        "below_50_count": len(weak_words),
        "dominant_weak_word": dominant_weak_word,
    }
