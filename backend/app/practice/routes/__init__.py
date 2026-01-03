from fastapi import APIRouter
from app.practice.routes.upload import upload_audio
from app.practice.routes.convert import convert_audio
from app.practice.routes.stt import speech_to_text
from app.practice.routes.evaluate import evaluate_practice

router = APIRouter(prefix="/practice", tags=["Practice"])

router.post("/upload")(upload_audio)
router.post("/convert/{file_id}")(convert_audio)
router.post("/stt/{file_id}")(speech_to_text)
router.post("/evaluate")(evaluate_practice)
