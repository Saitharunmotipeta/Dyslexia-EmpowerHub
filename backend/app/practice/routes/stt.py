from fastapi import HTTPException, Depends
from pydantic import BaseModel

from app.auth.dependencies import get_current_user_id


class BrowserSTTIn(BaseModel):
    text: str


def speech_to_text(
    file_id: str,  # ⚠️ kept ONLY for backward compatibility
    payload: BrowserSTTIn,
    user_id: int = Depends(get_current_user_id),
):
    """
    Browser-based STT.

    The browser performs speech recognition.
    Backend only receives recognized text.
    """

    recognized = payload.text.strip().lower()

    if not recognized:
        raise HTTPException(
            status_code=400,
            detail="Recognized text is empty",
        )

    print(
        f"🗣️ Browser STT | user={user_id} | file_id={file_id} | text='{recognized}'"
    )

    return {
        "file_id": file_id,
        "recognized_text": recognized,
        "source": "browser",
    }
