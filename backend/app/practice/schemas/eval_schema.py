from pydantic import BaseModel

class EvaluationRequest(BaseModel):
    word_id: int
    recognized_text: str
