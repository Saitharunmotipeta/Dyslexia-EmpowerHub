from sqlalchemy import Column, Integer, String, Index
from app.database.connection import Base
from sqlalchemy.orm import relationship


class Level(Base):
    __tablename__ = "levels"

    id = Column(Integer, primary_key=True, index=True)
    public_level_id = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    description = Column(String, default="")
    difficulty = Column(String, default="easy")
    order = Column(Integer, default=0)

    words = relationship("Word", back_populates="level")

    __table_args__ = (
        Index("idx_level_order", "order"),
    )
