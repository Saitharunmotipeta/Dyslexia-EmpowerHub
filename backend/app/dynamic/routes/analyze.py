from fastapi import Depends
from app.dynamic.schemas import DynamicAnalyzeIn, DynamicAnalyzeOut
from app.dynamic.services.analyzer import detect_type, normalize_text
from app.dynamic.services.tokenizer import tokenize_sentence
from app.dynamic.services.meaning import generate_meaning
from app.auth.dependencies import get_current_user_id


def analyze_dynamic_text(
    data: DynamicAnalyzeIn,
    user_id: int = Depends(get_current_user_id),
) -> DynamicAnalyzeOut:

    normalized_text = normalize_text(data.text)
    text_type = detect_type(normalized_text)

    words = (
        [normalized_text]
        if text_type == "word"
        else tokenize_sentence(normalized_text)
    )

    meaning = generate_meaning(normalized_text, text_type)

    return DynamicAnalyzeOut(
        type=text_type,
        words=words,
        meaning=meaning
    )

