# app/practice/routes/prac_automation.py

from fastapi import UploadFile, File, HTTPException
from app.practice.services.orchestrator_service import run_practice_flow


async def practice_auto(
    word_id: int,
    file: UploadFile = File(...)
):
    """
    Full practice automation:
    1. Save upload
    2. Convert → wav
    3. STT
    4. Evaluate similarity
    5. Update mastery status
    """
    try:
        return await run_practice_flow(word_id, file)

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
