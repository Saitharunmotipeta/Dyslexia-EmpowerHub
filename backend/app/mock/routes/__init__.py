from fastapi import APIRouter

from app.mock.routes.start import start_mock
from app.mock.routes.word import submit_mock_word
from app.mock.routes.result import get_mock_result
from app.mock.routes.report import download_mock_report_handler

router = APIRouter(prefix="/mock", tags=["Mock Test"])

router.post("/start")(start_mock)
router.post("/word")(submit_mock_word)
router.post("/result")(get_mock_result)
router.get("/report", response_model=None)(download_mock_report_handler)
