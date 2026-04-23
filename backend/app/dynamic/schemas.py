from pydantic import BaseModel
from typing import List, Literal


class DynamicAnalyzeIn(BaseModel):
    text: str


class DynamicAnalyzeOut(BaseModel):
    type: Literal["word", "sentence"]
    words: List[str]
    meaning: str


class DynamicEvaluateIn(BaseModel):
    expected_text: str
    recognized_text: str


class DynamicEvaluateOut(BaseModel):
    expected: str
    recognized: str
    score: float
    is_correct: bool


class DynamicAttemptCreate(BaseModel):
    text: str
    text_type: Literal["word", "sentence"]
    spoken: str
    score: float
    pace: float | None = None


class DynamicAttemptOut(BaseModel):
    attempt_id: str
    message: str