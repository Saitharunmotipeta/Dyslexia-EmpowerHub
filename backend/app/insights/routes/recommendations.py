# app/feedback/routes/recommendations.py

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.auth.dependencies import get_current_user_id

from app.insights.schemas import FeedbackIn, RecommendationOut
from app.insights.services.recommendations_service import recommend_next_step
from app.insights.services.weakness_engine import generate_weakness_heatmap


def recommendation_endpoint(
    data: FeedbackIn,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
    pattern: dict | None = None,
    alignment=None   # 🔥 NEW
) -> RecommendationOut:

    # -------------------------
    # 🔥 FETCH WEAKNESS DATA
    # -------------------------
    weakness_heatmap = generate_weakness_heatmap(db, user_id)

    # -------------------------
    # 🔥 EXTRACT MISTAKES FROM ALIGNMENT
    # -------------------------
    mistakes = []

    if alignment:
        for item in alignment:
            if item["type"] in ["substitution", "missing"]:
                if item.get("expected"):
                    mistakes.append(item["expected"])

    # remove duplicates
    mistakes = list(dict.fromkeys(mistakes))

    # -------------------------
    # 🔥 GENERATE RECOMMENDATION
    # -------------------------
    result = recommend_next_step(
        data=data,
        weakness_heatmap=weakness_heatmap,
        pattern=pattern,
        mistakes=mistakes   # 🔥 NEW
    )

    return result