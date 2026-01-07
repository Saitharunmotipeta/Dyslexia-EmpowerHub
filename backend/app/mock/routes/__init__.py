from fastapi import APIRouter

from app.mock.routes.start import start_mock
from app.mock.routes.word import submit_mock_word
from app.mock.routes.result import get_mock_result

router = APIRouter(prefix="/mock", tags=["Mock Test"])

router.post("/start")(start_mock)
router.post("/word")(submit_mock_word)
router.post("/result")(get_mock_result)
