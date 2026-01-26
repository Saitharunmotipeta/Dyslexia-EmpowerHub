import os
import uuid
from fastapi import UploadFile, File, HTTPException
from app.practice.schemas.upload_schema import AudioUploadResponse

BASE_UPLOAD_DIR = "temp/audio_uploads"
os.makedirs(BASE_UPLOAD_DIR, exist_ok=True)

ALLOWED_TYPES = {
    "audio/mpeg",
    "audio/mp4",
    "audio/webm",
    "audio/wav",
    "audio/ogg",
}


async def upload_audio(
    file: UploadFile,
    user_id: int,
) -> AudioUploadResponse:
    """
    Saves uploaded audio scoped to authenticated user.
    Caller MUST provide user_id explicitly.
    """

    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported audio format")

    user_dir = os.path.join(BASE_UPLOAD_DIR, str(user_id))
    os.makedirs(user_dir, exist_ok=True)

    file_id = str(uuid.uuid4())
    ext = file.filename.split(".")[-1]
    filepath = os.path.join(user_dir, f"{file_id}.{ext}")

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
