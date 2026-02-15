# app/learning/models/level_word.py

from sqlalchemy import (Column,Integer,ForeignKey,DateTime,Float,Boolean,Index)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.connection import Base


class LevelWord(Base):
    __tablename__ = "level_words"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"),nullable=False,index=True)
    word_id = Column(Integer,ForeignKey("words.id", ondelete="CASCADE"),nullable=False,index=True)
    attempts = Column(Integer, default=0)
    correct_attempts = Column(Integer, default=0)
    highest_score = Column(Float, default=0.0)
    mastery_score = Column(Float, default=0.0)
    is_mastered = Column(Boolean, default=False)
    last_similarity = Column(Float, default=0.0)
    last_practiced_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="level_words")
    word = relationship("Word", backref="user_progress")

    __table_args__ = (
        Index("idx_user_word_unique", "user_id", "word_id", unique=True),
    )