# app/practice/routes/prac_automation.py

from fastapi import UploadFile, File, HTTPException
from app.practice.services.orchestrator_service import run_practice_flow


async def practice_auto(
    word_id: int,
    file: UploadFile = File(...)
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
        result = await run_practice_flow(word_id, file)

        return {
            "status": "success",
            "data": result
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
