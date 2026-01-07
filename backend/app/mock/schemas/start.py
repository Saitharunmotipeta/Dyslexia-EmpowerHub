from pydantic import BaseModel
from typing import List


class MockWord(BaseModel):
    id: int
    text: str


class MockStartResponse(BaseModel):
    attempt_id: int
    level_id: int
    words: List[MockWord]
    message: str
    
