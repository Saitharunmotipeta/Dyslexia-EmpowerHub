# app/practice/routes/prac_automation.py

from fastapi import UploadFile, File, HTTPException, Depends
from app.practice.services.orchestrator_service import run_practice_flow
from app.auth.dependencies import get_current_user_id


async def practice_auto(
    word_id: int,
    level_id: int,
    file: UploadFile = File(...),
    user_id: int = Depends(get_current_user_id),
):
    """
    Practice Automation Endpoint

    Pipeline:
    1️⃣ Save uploaded audio
    2️⃣ Convert → WAV
    3️⃣ Speech-to-Text
    4️⃣ Evaluate pronunciation
    5️⃣ Update progress tracking
    6️⃣ Generate Feedback
    7️⃣ Generate Recommendation
    """

    try:
        result = await run_practice_flow(
            word_id=word_id,
            file=file,
            user_id=user_id,
            level_id = level_id,
            )

        return {
            "status": "success",
            "data": result
        }

    except HTTPException:
        raise

    # except Exception as e:
    #     raise HTTPException(
    #         status_code=500,
    #         detail=str(e)
    #     )
