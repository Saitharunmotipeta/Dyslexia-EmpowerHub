from pydantic import BaseModel
from typing import Optional


class WordStatusOut(BaseModel):
    id: int
    text: str
    phonetics: str
    syllables: str      # 🚨 REQUIRED
    difficulty: str 
    # image_url: Optional[str]
    is_mastered: bool
    mastery_score: float
    attempts: int

    class Config:
        orm_mode = True
