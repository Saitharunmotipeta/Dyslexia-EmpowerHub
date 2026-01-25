from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connection import Base


class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)

    phonetics = Column(String, default="")
    syllables = Column(String, default="")
    difficulty = Column(String, default="easy")
    image_url = Column(String, nullable=True, default=None)

    level_id = Column(Integer, ForeignKey("levels.id"), nullable=False)

    level = relationship("Level", backref="words")
