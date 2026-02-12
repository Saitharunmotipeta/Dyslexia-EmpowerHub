from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, Index
from sqlalchemy.orm import relationship

from app.database.connection import Base


class DynamicAttempt(Base):
    __tablename__ = "dynamic_attempts"

    id = Column(Integer, primary_key=True, index=True)
    public_attempt_id = Column(String(15), unique=True, nullable=False, index=True)

    # 🔗 Relation to User
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # 📘 Content
    text = Column(Text, nullable=False)
    text_type = Column(String(20), nullable=False)  # word / phrase / sentence

    # 🗣 Practice
    spoken = Column(Text, nullable=False)
    score = Column(Float, nullable=False)
    pace = Column(Float, nullable=True)

    # ⏱ Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # ORM Relationship
    user = relationship("User", back_populates="dynamic_attempts")


# Composite index for performance
Index(
    "idx_dynamic_user_created",
    DynamicAttempt.user_id,
    DynamicAttempt.created_at.desc()
)
