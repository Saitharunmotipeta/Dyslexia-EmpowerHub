from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database.connection import Base


class MockWord(Base):
    __tablename__ = "mock_words"

    id = Column(Integer, primary_key=True, index=True)

    # Link to level
    level_id = Column(Integer, ForeignKey("levels.id"), nullable=False, index=True)

    # Word data
    text = Column(String, nullable=False)
    phonetics = Column(String, nullable=True)
    syllables = Column(String, nullable=True)
    difficulty = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())