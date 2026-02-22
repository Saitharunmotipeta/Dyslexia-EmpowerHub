from fastapi import APIRouter
from app.practice.routes.evaluate import evaluate_practice
from app.practice.routes.prac_automation import practice_auto
from app.practice.routes.phoneme import analyze_phoneme_handler

router = APIRouter(prefix="/practice", tags=["Practice"])

router.post("/evaluate")(evaluate_practice)
router.post("/auto")(practice_auto)
router.post(
    "/phoneme",
    summary="Extract phonemes from text",
    response_model=None
)(analyze_phoneme_handler)

