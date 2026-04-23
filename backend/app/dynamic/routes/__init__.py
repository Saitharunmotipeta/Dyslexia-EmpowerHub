from fastapi import APIRouter, Depends

from app.dynamic.routes.analyze import analyze_dynamic_text
from app.dynamic.routes.attempt import save_dynamic_attempt

from app.dynamic.routes.evaluate_audio import evaluate_dynamic_text

from app.dynamic.schemas import (
    DynamicEvaluateIn,
    DynamicEvaluateOut,
)

from app.auth.dependencies import get_current_user_id

router = APIRouter(prefix="/dynamic", tags=["Dynamic Learning"])


# Existing routes
router.post("/analyze")(analyze_dynamic_text)
router.post("/attempt")(save_dynamic_attempt)


# ✅ New Evaluate Route
@router.post("/evaluate", response_model=DynamicEvaluateOut)
async def evaluate_dynamic_route(
    payload: DynamicEvaluateIn,
    user_id: int = Depends(get_current_user_id),
):
    _ = user_id  # enforce auth

    result = evaluate_dynamic_text(
        expected_text=payload.expected_text,
        recognized_text=payload.recognized_text,
    )

    return DynamicEvaluateOut(
        expected=result.expected,
        recognized=result.recognized,
        score=result.score,
        is_correct=result.is_correct,
    )