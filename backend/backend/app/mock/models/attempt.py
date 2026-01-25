from sqlalchemy import Column, Integer, ForeignKey, DateTime, JSON, String
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.sql import func

from app.database.connection import Base


class MockAttempt(Base):
    __tablename__ = "mock_attempts"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    level_id = Column(Integer, ForeignKey("levels.id"), nullable=False)
    attempt_code = Column(Integer, unique=True, index=True, nullable=False)

    # status lifecycle: started → completed
    status = Column(String, default="started", nullable=False)

    # Stores per-word results
    # Example:
    # {
    #   "words": [
    #     {
    #       "word_id": 12,
    #       "expected": "apple",
    #       "recognized": "aple",
    #       "score": 82.5,
    #       "verdict": "good",
    #       "time_taken": 97
    #     }
    #   ]
    # }
    results = Column(MutableDict.as_mutable(JSON),nullable=False,default=lambda: {"words": []})

    total_score = Column(Integer, nullable=True)
    verdict = Column(String, nullable=True)

    started_at = Column(DateTime(timezone=True), server_default=func.now())  # ✅ ADD THIS
    completed_at = Column(DateTime(timezone=True), nullable=True, default=None, onupdate=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_accessed_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
