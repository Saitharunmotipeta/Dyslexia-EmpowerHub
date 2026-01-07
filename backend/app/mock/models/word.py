# app/mock/models/word.py

from sqlalchemy import Column, Integer, String
from app.database.connection import Base

class MockWord(Base):
    __tablename__ = "mock_words"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String, index=True)
    level_id = Column(Integer, nullable=False)
    word = Column(String, nullable=False)
