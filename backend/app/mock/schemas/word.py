from pydantic import BaseModel


class MockWordRequest(BaseModel):
    public_attempt_id: str
    word_id: int
    spoken: str

class MockWordResponse(BaseModel):
    word_id: int
    public_attempt_id: str
    spoken: str
    score: float
    verdict: str
    message: str
    recognized_text: str
