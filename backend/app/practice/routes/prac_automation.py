from fastapi import HTTPException, Depends
from pydantic import BaseModel

from app.practice.services.orchestrator_service import run_practice_flow
from app.auth.dependencies import get_current_user_id


class PracticeAutoIn(BaseModel):
    word_id: int
    level_id: int
    spoken: str


async def practice_auto(
    payload: PracticeAutoIn,
    user_id: int = Depends(get_current_user_id),
):
    """
    Practice Automation (Browser-based STT)

    Browser handles speech recognition.
    Backend handles evaluation + learning logic.
    """

    try:
        result = await run_practice_flow(
            word_id=payload.word_id,
            level_id=payload.level_id,
            spoken=payload.spoken,
            user_id=user_id,
        )

        return {
            "status": "success",
            "data": result,
        }

    except HTTPException:
        raise
