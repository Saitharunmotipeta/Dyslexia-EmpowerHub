from datetime import datetime, timedelta


MAX_WORD_TIME = timedelta(seconds=105)  # 1m 45s


def is_time_exceeded(last_accessed: datetime) -> bool:
    return datetime.utcnow() - last_accessed > MAX_WORD_TIME
