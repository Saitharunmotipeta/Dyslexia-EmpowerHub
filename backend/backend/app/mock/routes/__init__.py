from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user_id
from app.mock.routes.start import start_mock
from app.mock.routes.word import submit_mock_word
from app.mock.routes.result import get_mock_result
from app.mock.routes.report import download_mock_report_handler
# from app.mock.routes.automation import (start_automation,submit_word_automation,complete_automation)

router = APIRouter(prefix="/mock", tags=["Mock Test"],dependencies=[Depends(get_current_user_id)])

router.post("/start")(start_mock)
router.post("/word")(submit_mock_word)
router.post("/result")(get_mock_result)
router.get("/report", response_model=None)(download_mock_report_handler)
# router.post("/automation/start", response_model=None)(start_automation)
# router.post("/automation/submit-word")(submit_word_automation)
# router.post("/automation/complete")(complete_automation)
