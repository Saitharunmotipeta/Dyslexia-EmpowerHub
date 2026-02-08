from pydantic import BaseModel
from typing import List, Dict

class MockResultRequest(BaseModel):
    attempt_id: int

class MockResultResponse(BaseModel):
    attempt_id: int
    score: float
    verdict: str
    words: List[Dict]
    message: str
    recommendations: List[Dict]
    confidence: float
    metrics: Dict[str, float]
    tips: List[str]
    next_steps: List[str]
    detailed_feedback: List[Dict]
    