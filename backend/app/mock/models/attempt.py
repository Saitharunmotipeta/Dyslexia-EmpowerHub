from sqlalchemy import (Column,Integer,ForeignKey,DateTime,JSON,String,Float,Index)
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.connection import Base

class MockAttempt(Base):
    __tablename__ = "mock_attempts"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"),nullable=False,index=True)
    level_id = Column(Integer,ForeignKey("levels.id", ondelete="CASCADE"),nullable=False,index=True)
    public_attempt_id = Column(String(20), unique=True, index=True, nullable=False)
    status = Column(String, default="started", nullable=False)
    results = Column(MutableDict.as_mutable(JSON),nullable=False,default=lambda: {"words": []})
    total_score = Column(Float, nullable=True)
    verdict = Column(String, nullable=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    user = relationship("User", backref="mock_attempts")
    level = relationship("Level")

    __table_args__ = (
        Index("idx_mock_user_level", "user_id", "level_id"),
    )
