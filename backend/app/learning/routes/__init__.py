# app/learning/routes/__init__.py
from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.orm import Session
from typing import List


from app.database.connection import SessionLocal
from app.auth.dependencies import get_current_user_id
from app.learning.schemas.level import LevelOut
from app.learning.schemas.word import WordStatusOut

from .levels import (
    get_levels_handler,
    get_words_for_level_handler
)
from app.learning.routes.words import update_word_status_handler
from app.learning.routes.tts import tts_word_handler


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
router.get("/tts/{word_id}")(
    lambda word_id,
           pace=Query(85),
           db=Depends(get_db):
        tts_word_handler(db, word_id, pace)
)
