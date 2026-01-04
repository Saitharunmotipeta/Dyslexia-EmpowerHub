from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Boolean
from sqlalchemy.orm import relationship
from app.database.connection import Base


class LevelWord(Base):
    __tablename__ = "level_words"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, nullable=False)
    word_id = Column(Integer, ForeignKey("words.id"), nullable=False)
    level_id = Column(Integer, ForeignKey("levels.id"), nullable=False)

    image_url = Column(String, nullable=True, default=None)

    attempts = Column(Integer, default=0)
    correct_attempts = Column(Integer, default=0)

    mastery_score = Column(Float, default=0.0)
    is_mastered = Column(Boolean, default=False)

    last_similarity = Column(Float, default=0.0)
    last_practiced_at = Column(DateTime, nullable=True)

    word = relationship("Word", backref="user_links")
