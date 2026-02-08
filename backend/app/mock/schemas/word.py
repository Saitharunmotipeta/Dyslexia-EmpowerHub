from pydantic import BaseModel


class MockWordRequest(BaseModel):
    attempt_id: int
    word_id: int
    spoken: str

class MockWordResponse(BaseModel):
    word_id: int
    attempt_id: int
    spoken: str
    score: float
    verdict: str
    message: str
    recognized_text: str
