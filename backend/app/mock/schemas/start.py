from pydantic import BaseModel
from typing import List


class MockWord(BaseModel):
    id: int
    word: str   # ⚠️ FIX: backend returns "word", not "text"


class MockStartResponse(BaseModel):
    public_attempt_id: int
    words: List[MockWord]
    message: str
