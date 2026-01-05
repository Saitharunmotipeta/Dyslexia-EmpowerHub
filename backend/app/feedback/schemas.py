from pydantic import BaseModel


class FeedbackIn(BaseModel):
    word: str
    spoken: str
    similarity: float
    attempts: int
    pace: str | None = "medium"


class FeedbackOut(BaseModel):
    verdict: str
    score: float
    feedback: list[str]
    confidence_tip: str
