# app/learning/routes/__init__.py
from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.orm import Session
from fastapi import UploadFile, File
from typing import List


from app.database.connection import SessionLocal
from app.auth.dependencies import get_current_user_id
from app.learning.schemas.level import LevelOut
from app.learning.schemas.word import WordStatusOut
# from app.learning.routes.learning_automation import router as automation_router

from .levels import (
    get_levels_handler,
    get_words_for_level_handler
)
from app.learning.routes.words import update_word_status_handler
from app.learning.routes.tts import tts_word_handler
from app.learning.routes.learning_automation import learning_automation_handler


router = APIRouter(prefix="/learning", tags=["Learning"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# LEVEL LIST
router.get("/levels", response_model=List[LevelOut])(
    lambda db=Depends(get_db): get_levels_handler(db)
)


# WORD LIST PER LEVEL
router.get("/levels/{level_id}/words", response_model=List[WordStatusOut])(
    lambda level_id, db=Depends(get_db), user_id=Depends(get_current_user_id):
        get_words_for_level_handler(level_id, db, user_id)
)


# UPDATE STATUS
@router.post("/words/{word_id}/update_status")
def update_word_status_endpoint(
    word_id: int,
    is_mastered: bool = Body(...),
    mastery_score: float = Body(...),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    return update_word_status_handler(
        db=db,
        user_id=user_id,
        word_id=word_id,
        is_mastered=is_mastered,
        mastery_score=mastery_score,
    )


# TTS
@router.get("/tts/{word_id}")
def tts_word(
    word_id: int,
    pace_mode: str = Query(
        ...,
        description="slow | medium | fast | custom"
    ),
    pace_value: int | None = Query(
        None,
        ge=30,
        le=200,
        description="Required only when pace_mode=custom"
    ),
    db: Session = Depends(get_db),
):
    return tts_word_handler(
        db=db,
        word_id=word_id,
        pace_mode=pace_mode,
        pace_value=pace_value,
    )


@router.post(
    "/learn-auto",
    summary="Learning Automation Endpoint",
)
async def learn_auto(
    level_id: int,
    word_id: int,
    pace_mode: str = Query("medium", regex="^(slow|medium|fast|custom)$"),
    pace_value: int | None = Query(None, ge=40, le=200),
    file: UploadFile = File(...),
    user_id: int = Depends(get_current_user_id),
):
    return await learning_automation_handler(
        level_id=level_id,
        word_id=word_id,
        user_id=user_id,
        pace_mode=pace_mode,
        pace_value=pace_value,
        file=file,
    )