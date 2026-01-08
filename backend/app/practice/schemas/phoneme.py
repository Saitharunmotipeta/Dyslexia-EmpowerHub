from pydantic import BaseModel

class PhonemeRequest(BaseModel):
    text: str
