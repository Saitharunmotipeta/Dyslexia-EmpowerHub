from sqlalchemy import Column, Integer, String
from app.database.connection import Base


class Level(Base):
    __tablename__ = "levels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, default="")
    difficulty = Column(String, default="easy")
    order = Column(Integer, default=0)
