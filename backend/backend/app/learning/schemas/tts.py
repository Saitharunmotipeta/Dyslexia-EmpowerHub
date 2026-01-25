from pydantic import BaseModel


class TTSRequest(BaseModel):
    text: str
    speed: str = "medium"


class TTSResponse(BaseModel):
    audio_url: str
