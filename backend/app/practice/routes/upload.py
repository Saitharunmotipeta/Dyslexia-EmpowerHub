import os
import uuid
from fastapi import UploadFile, File, HTTPException
from app.practice.schemas.upload_schema import AudioUploadResponse

UPLOAD_DIR = "temp/audio_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_TYPES = {
    "audio/mpeg",
    "audio/mp4",
    "audio/webm",
    "audio/wav",
    "audio/ogg",
}


async def upload_audio(file: UploadFile = File(...)) -> AudioUploadResponse:
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported audio format")

    file_id = str(uuid.uuid4())
    ext = file.filename.split(".")[-1]
    filepath = os.path.join(UPLOAD_DIR, f"{file_id}.{ext}")

    try:
        with open(filepath, "wb") as f:
            f.write(await file.read())
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to save audio")

    return AudioUploadResponse(
        file_id=file_id,
        original_filename=file.filename,
        content_type=file.content_type,
        message="Audio uploaded successfully",
    )
