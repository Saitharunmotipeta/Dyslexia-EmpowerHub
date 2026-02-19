from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user_id
from app.chatbot.routes.chat import chat_handler

router = APIRouter(prefix="/chatbot",tags=["Chatbot"],dependencies=[Depends(get_current_user_id)],)

router.post("/chat")(chat_handler)
