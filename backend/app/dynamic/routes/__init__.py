from fastapi import APIRouter
from app.dynamic.routes.analyze import analyze_dynamic_text

router = APIRouter(prefix="/dynamic", tags=["Dynamic Learning"])

router.post("/analyze")(analyze_dynamic_text)
router.post("/attempt")(analyze_dynamic_text) # Placeholder, will be replaced with save_dynamic_attempt
