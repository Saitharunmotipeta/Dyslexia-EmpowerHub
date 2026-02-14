from fastapi import APIRouter
from app.dynamic.routes.analyze import analyze_dynamic_text
from app.dynamic.routes.attempt import save_dynamic_attempt

router = APIRouter(prefix="/dynamic", tags=["Dynamic Learning"])

router.post("/analyze")(analyze_dynamic_text)
router.post("/attempt")(save_dynamic_attempt) # Placeholder, will be replaced with save_dynamic_attempt
