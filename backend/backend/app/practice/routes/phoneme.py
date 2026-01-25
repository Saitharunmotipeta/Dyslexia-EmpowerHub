from fastapi import HTTPException
from app.practice.schemas.phoneme import PhonemeRequest
from app.practice.services.phoneme_service import extract_phonemes

def analyze_phoneme_handler(payload: PhonemeRequest):
    text = payload.text.strip()

    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    phonemes = extract_phonemes(text)

    if phonemes is None:
        raise HTTPException(
            status_code=500,
            detail="Phoneme extraction failed"
        )

    return {
        "status": "success",
        "input": text,
        "phonemes": phonemes
    }
