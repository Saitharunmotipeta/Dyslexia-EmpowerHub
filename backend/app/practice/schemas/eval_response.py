from pydantic import BaseModel

class EvaluationResponse(BaseModel):
    word_id: int
    expected: str
    recognized: str
    score: float
    is_correct: bool
