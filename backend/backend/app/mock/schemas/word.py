from pydantic import BaseModel


class MockWordResponse(BaseModel):
    word_id: int
    score: float
    verdict: str
    message: str
    recognized_text: str

    
