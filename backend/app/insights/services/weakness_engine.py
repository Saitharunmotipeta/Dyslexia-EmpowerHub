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
        return {
            "heatmap": counters,
            "top_weakness": None,
            "message": None
        }

    # 🔥 convert to percentage
    percentages = {
        k: round((v / total) * 100, 2)
        for k, v in counters.items()
    }

    # 🔥 identify top weakness
    top_weakness = max(percentages, key=percentages.get)

    # 🔥 ignore weak signals (<15%)
    if percentages[top_weakness] < 15:
        top_weakness = None

    # 🔥 map to actionable message (VERY IMPORTANT)
    weakness_messages = {
        "initial_sound": "You often miss starting sounds. Begin words slowly.",
        "vowel": "You confuse vowel sounds. Open your mouth clearly.",
        "final_sound": "You drop ending sounds. finish words fully.",
        "far_off": "Some words are very different. Break them into parts.",
    }

    message = weakness_messages.get(top_weakness) if top_weakness else None

    return {
        "heatmap": percentages,
        "top_weakness": top_weakness,
        "message": message
    }