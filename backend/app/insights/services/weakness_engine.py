from sqlalchemy.orm import Session

from app.mock.models.attempt import MockAttempt


def generate_weakness_heatmap(db: Session, user_id: int):

    attempts = (
        db.query(MockAttempt)
        .filter(
            MockAttempt.user_id == user_id,
            MockAttempt.status == "completed"
        )
        .all()
    )

    counters = {
        "initial_sound": 0,
        "vowel": 0,
        "final_sound": 0,
        "far_off": 0
    }

    total = 0

    for attempt in attempts:

        results = attempt.results or {}
        words = results.get("words", [])

        for w in words:

            phonetics = w.get("phonetics", {})
            insights = phonetics.get("insights", {})

            if insights.get("initial_sound") == "mismatch":
                counters["initial_sound"] += 1

            if insights.get("vowel") == "confusion":
                counters["vowel"] += 1

            if insights.get("final_sound") == "mismatch":
                counters["final_sound"] += 1

            if w.get("score", 100) < 50:
                counters["far_off"] += 1

            total += 1

    if total == 0:
        return counters

    # convert to percentage
    return {
        k: round((v / total) * 100, 2)
        for k, v in counters.items()
    }