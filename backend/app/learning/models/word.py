from sqlalchemy import (Column,Integer,String,ForeignKey,Float,Index)
from sqlalchemy.orm import relationship
from app.database.connection import Base


class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    public_word_id = Column(String(20), unique=True, nullable=False, index=True)
    text = Column(String, nullable=False)
    content_type = Column(String(20), nullable=False)  
    phonetics = Column(String, default="")
    syllables = Column(String, default="")
    syllable_count = Column(Integer, default=0)
    difficulty = Column(String, default="easy")
    complexity_score = Column(Float, default=0.0)
    level_id = Column(Integer, ForeignKey("levels.id", ondelete="CASCADE"), nullable=False)

    level = relationship("Level", back_populates="words")

    __table_args__ = (
        Index("idx_word_level_difficulty", "level_id", "difficulty"),
    )