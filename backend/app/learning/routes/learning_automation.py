# app/learning/routes/learning_automation.py

from fastapi import UploadFile, File, Depends
from app.auth.dependencies import get_current_user_id
from app.learning.services.orchestration_logic import run_learning_pipeline


async def learning_automation_handler(
    level_id: int,
    word_id: int,
    pace_mode: str,
    pace_value: int | None,
    file: UploadFile = File(...),
    user_id: int = Depends(get_current_user_id),
):
    """
    HTTP entry point only.
    Business logic lives in service layer.
    """
    return await run_learning_pipeline(
        user_id=user_id,
        level_id=level_id,
        word_id=word_id,
        pace_mode=pace_mode,
        pace_value=pace_value,
        file=file,
    )
