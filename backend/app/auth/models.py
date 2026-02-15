from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from app.database.connection import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    role = Column(String, default="student", nullable=False)

    password_hash = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    last_login_at = Column(DateTime, nullable=True)
    last_active_at = Column(DateTime, nullable=True)

    tts_rate = Column(Integer, default=100)

    streak_days = Column(Integer, default=0)
    total_login_days = Column(Integer, default=0)

    points = Column(Integer, default=0)
    badges = Column(String, default="")
    achievements = Column(String, default="")

    total_time_spent = Column(Integer, default=0)
    courses_completed = Column(Integer, default=0)

    dynamic_attempts = relationship(
    "DynamicAttempt",
    back_populates="user",
    cascade="all, delete-orphan"
)

level_words = relationship(
    "LevelWord",
    back_populates="user",
    cascade="all, delete-orphan"
)
