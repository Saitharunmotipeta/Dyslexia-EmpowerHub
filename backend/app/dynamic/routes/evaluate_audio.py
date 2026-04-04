from fastapi import Depends, HTTPException, UploadFile, File, Form

from app.auth.dependencies import get_current_user_id
from app.practice.services.eval_service import evaluate_similarity
from app.practice.services.speech_client import recognize_speech
from app.practice.schemas.eval_response import EvaluationResponse


def evaluate_dynamic_audio(
    expected_text: str = Form(...),
    file: UploadFile = File(...),
    user_id: int = Depends(get_current_user_id),
) -> EvaluationResponse:
    """
    Speech evaluation for Dynamic Learning using the user's own analyzed text.
    Does not require a vocabulary word_id or LevelWord row.
    """
    expected = (expected_text or "").strip()
    if not expected:
        raise HTTPException(status_code=400, detail="expected_text is required")

    try:
        file.file.seek(0, 2)
        audio_size = file.file.tell()
        file.file.seek(0)
    except Exception:
        audio_size = -1
    if audio_size == 0:
        raise HTTPException(
            status_code=400,
            detail="Empty audio upload. Record again and ensure the browser has microphone access.",
        )

    try:
        speech_result = recognize_speech(file)
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Speech recognition failed: {e!s}",
        ) from e

    spoken = (
        speech_result.get("recognized_text")
        or speech_result.get("text")
        or speech_result.get("transcript")
        or ""
    )
    if isinstance(spoken, str):
        spoken = spoken.strip()
    else:
        spoken = str(spoken or "")

    score, verdict = evaluate_similarity(expected, spoken)

    return EvaluationResponse(
        word_id=0,
        expected=expected,
        recognized=spoken,
        score=score,
        verdict=verdict,
        is_correct=(score >= 80.0),
    )
