import time
import threading
from typing import Dict, Optional


class AICache:
    """
    Thread-safe in-memory cache with TTL.
    Suitable for production until Redis is needed.
    """

    def __init__(self, ttl_seconds: int = 6 * 60 * 60):
        # default TTL = 6 hours
        self._ttl = ttl_seconds
        self._store: Dict[str, tuple[str, float]] = {}
        self._lock = threading.Lock()

    def get(self, key: str) -> Optional[str]:
        now = time.time()

        with self._lock:
            entry = self._store.get(key)
            if not entry:
                return None

            value, expires_at = entry
            if expires_at < now:
                # expired
                del self._store[key]
                return None

            return value

    def set(self, key: str, value: str) -> None:
        expires_at = time.time() + self._ttl

        with self._lock:
            self._store[key] = (value, expires_at)


# 🔒 Single cache instance (module-level, safe)
meaning_cache = AICache()
