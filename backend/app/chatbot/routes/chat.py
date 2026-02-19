from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.auth.dependencies import get_current_user_id
from app.chatbot.schemas.chat_request import ChatRequest
from app.chatbot.services.chat_service import handle_chat


def chat_handler(
    request: ChatRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    return handle_chat(
        message=request.message,
        user_id=user_id,
        db=db,
    )
