from pydantic import BaseModel
from typing import List, Literal


class DynamicAnalyzeIn(BaseModel):
    text: str


class DynamicAnalyzeOut(BaseModel):
    type: Literal["word", "sentence"]
    words: List[str]
    meaning: str
