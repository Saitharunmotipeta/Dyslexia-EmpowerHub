from pydantic import BaseModel
from typing import Literal


class ChatResponse(BaseModel):
    reply: str
    mode: Literal["context", "guidance", "general"]
