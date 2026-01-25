from pydantic import BaseModel


class LevelOut(BaseModel):
    id: int
    name: str
    description: str
    difficulty: str
    order: int
    total_words: int
    mastered_words: int
    mastered_percentage: float

    class Config:
        orm_mode = True
