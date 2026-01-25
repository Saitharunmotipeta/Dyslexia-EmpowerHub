from pydantic import BaseModel

class STTResponse(BaseModel):
    file_id: str
    recognized_text: str
