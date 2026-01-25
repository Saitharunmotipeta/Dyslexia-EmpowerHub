from pydantic import BaseModel
from typing import List, Optional


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

class RecommendationOut(BaseModel):
    recommendation: str  # machine-friendly key
    headline: str        # user-friendly title
    explanation: str     # short reason in plain english
    confidence: float    # 0–1 likelihood
    next_steps: List[str]
    metrics_used: Optional[dict] = None

