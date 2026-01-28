import uuid
from fastapi import UploadFile, HTTPException

from app.practice.schemas.upload_schema import AudioUploadResponse
from app.core.paths import AUDIO_UPLOAD_DIR


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

    # Create user-scoped directory
    user_dir = AUDIO_UPLOAD_DIR / str(user_id)
    user_dir.mkdir(parents=True, exist_ok=True)

    file_id = str(uuid.uuid4())
    ext = file.filename.split(".")[-1]
    filepath = user_dir / f"{file_id}.{ext}"

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
