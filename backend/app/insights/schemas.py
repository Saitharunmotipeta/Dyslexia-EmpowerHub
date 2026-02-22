from pydantic import BaseModel
from typing import List, Optional, Literal


class FeedbackIn(BaseModel):
    mode: Literal["static", "dynamic"]
    content_type: Literal["word", "phrase", "sentence"]
    text: str
    spoken: str
    score: float
    attempts: int
    pace: float | None = 0.9


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