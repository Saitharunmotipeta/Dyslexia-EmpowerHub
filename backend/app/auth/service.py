from sqlalchemy.orm import Session
from datetime import datetime, date

from app.auth.models import User
from app.auth.utils import hash_password, verify_password, create_access_token
from sqlalchemy import func
from app.learning.models.level_word import LevelWord
from app.learning.models.word import Word
from app.dynamic.models.dynamic_attempt import DynamicAttempt


def register_user(db: Session, name: str, email: str, password: str):
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        return None

    user = User(
        name=name,
        email=email,
        password_hash=hash_password(password),
        streak_days=0,
        total_login_days=0,
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.password_hash):
        return None

    today = date.today()

    if user.last_login_at:
        last_login_date = user.last_login_at.date()
        if today == last_login_date:
            pass
        elif (today - last_login_date).days == 1:
            user.streak_days += 1
        else:
            user.streak_days = 1
    else:
        user.streak_days = 1

    user.last_login_at = datetime.utcnow()
    user.last_active_at = datetime.utcnow()
    user.total_login_days += 1

    db.commit()

    token = create_access_token({"sub": str(user.id)})
    return token, user

def get_user_analytics(
    db,
    user_id: int,
    content_type: str | None = None,
    source: str = "both",  # static | dynamic | both
):
    # Word = db.get_bind().mapper_registry.mapped_classes[0]
    dynamic_query = db.query(DynamicAttempt).filter(
        DynamicAttempt.user_id == user_id
    )

    if content_type:
        dynamic_query = dynamic_query.filter(
            DynamicAttempt.text_type == content_type
        )

    dynamic_attempts = dynamic_query.all()

    total_dynamic = len(dynamic_attempts)
    correct_dynamic = len([a for a in dynamic_attempts if a.score >= 80])
    wrong_dynamic = total_dynamic - correct_dynamic

    avg_dynamic_score = (
        sum(a.score for a in dynamic_attempts) / total_dynamic
        if total_dynamic > 0 else 0
    )

    # -------------------------
    # 🔥 STATIC (LEVEL WORDS)
    # -------------------------
    level_words = db.query(LevelWord).filter(
        LevelWord.user_id == user_id
    ).all()

    total_static_attempts = sum(lw.attempts for lw in level_words)
    correct_static = sum(lw.correct_attempts for lw in level_words)
    wrong_static = total_static_attempts - correct_static

    completed_words = len([lw for lw in level_words if lw.is_mastered])
    in_progress_words = len([
        lw for lw in level_words if lw.attempts > 0 and not lw.is_mastered
    ])

    # 🔥 TRUE TOTAL WORDS
    total_words = db.query(Word).count()

    not_started_words = total_words - len(level_words)

    # -------------------------
    # 🔥 COMBINE BASED ON SOURCE
    # -------------------------
    if source == "dynamic":
        total_attempts = total_dynamic
        correct_attempts = correct_dynamic
        wrong_attempts = wrong_dynamic
        avg_score = avg_dynamic_score

    elif source == "static":
        total_attempts = total_static_attempts
        correct_attempts = correct_static
        wrong_attempts = wrong_static
        avg_score = (
            (correct_static / total_static_attempts * 100)
            if total_static_attempts > 0 else 0
        )

    else:  # both
        total_attempts = total_dynamic + total_static_attempts
        correct_attempts = correct_dynamic + correct_static
        wrong_attempts = wrong_dynamic + wrong_static

        avg_score = (
            (avg_dynamic_score + (
                (correct_static / total_static_attempts * 100)
                if total_static_attempts else 0
            )) / 2
        )

    # -------------------------
    # 🔥 PRACTICE PER DAY
    # -------------------------
    # dynamic
    dynamic_per_day = (
        db.query(
            func.date(DynamicAttempt.created_at).label("date"),
            func.count(DynamicAttempt.id).label("count")
        )
        .filter(DynamicAttempt.user_id == user_id)
        .group_by(func.date(DynamicAttempt.created_at))
        .all()
    )

    dynamic_map = {str(row.date): row.count for row in dynamic_per_day}

    # static (approx)
    static_map = {}
    for lw in level_words:
        if lw.last_practiced_at:
            d = str(lw.last_practiced_at.date())
            static_map[d] = static_map.get(d, 0) + 1

    # merge
    all_dates = set(dynamic_map.keys()) | set(static_map.keys())
    practice_per_day_data = []

    for d in sorted(all_dates):
        val = {
            "date": d,
            "dynamic": dynamic_map.get(d, 0),
            "static": static_map.get(d, 0),
        }

        if source == "dynamic":
            val["count"] = val["dynamic"]
        elif source == "static":
            val["count"] = val["static"]
        else:
            val["count"] = val["dynamic"] + val["static"]

        practice_per_day_data.append(val)

    # -------------------------
    # 🔥 IMPROVEMENT (DYNAMIC ONLY)
    # -------------------------
    improvement = (
        db.query(
            func.date(DynamicAttempt.created_at).label("date"),
            func.avg(DynamicAttempt.score).label("avg_score")
        )
        .filter(DynamicAttempt.user_id == user_id)
        .group_by(func.date(DynamicAttempt.created_at))
        .order_by(func.date(DynamicAttempt.created_at))
        .all()
    )

    improvement_data = [
        {"date": str(row.date), "avg_score": round(row.avg_score, 2)}
        for row in improvement
    ]

    daily_improvement = {"score_diff": 0, "trend": "stable"}

    if len(improvement_data) >= 2:
        last = improvement_data[-1]["avg_score"]
        prev = improvement_data[-2]["avg_score"]
        diff = round(last - prev, 2)

        daily_improvement = {
            "score_diff": diff,
            "trend": "up" if diff > 0 else "down" if diff < 0 else "stable"
        }

    # -------------------------
    # 🔥 TYPE DISTRIBUTION
    # -------------------------
    dynamic_counts = {t: 0 for t in ["word", "phrase", "sentence"]}

    result = (
        db.query(
            DynamicAttempt.text_type,
            func.count(DynamicAttempt.id)
        )
        .filter(DynamicAttempt.user_id == user_id)
        .group_by(DynamicAttempt.text_type)
        .all()
    )

    for t, count in result:
        dynamic_counts[t] = count

    static_counts = {
        "word": total_words,
        "phrase": 0,
        "sentence": 0
    }

    if source == "dynamic":
        type_data = dynamic_counts
    elif source == "static":
        type_data = static_counts
    else:
        type_data = {
            k: dynamic_counts.get(k, 0) + static_counts.get(k, 0)
            for k in dynamic_counts
        }

    # -------------------------
    # 🔥 FINAL RESPONSE
    # -------------------------
    return {
        "summary": {
            "total_attempts": total_attempts,
            "correct_attempts": correct_attempts,
            "wrong_attempts": wrong_attempts,
            "avg_score": round(avg_score, 2),

            "words": {
                "total": total_words,
                "completed": completed_words,
                "in_progress": in_progress_words,
                "not_started": not_started_words
            }
        },

        "practice_per_day": practice_per_day_data,

        "improvement": {
            "trend": improvement_data,
            "daily": daily_improvement
        },

        "type_distribution": type_data
    }