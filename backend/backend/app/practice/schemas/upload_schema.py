from pydantic import BaseModel


class AudioUploadResponse(BaseModel):
    file_id: str
    original_filename: str
    content_type: str
    message: str
