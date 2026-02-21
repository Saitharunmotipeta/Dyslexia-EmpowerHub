from pydantic import BaseModel
from typing import List, Dict

class MockResultRequest(BaseModel):
    public_attempt_id: str

class MockResultResponse(BaseModel):
    public_attempt_id: str
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
    