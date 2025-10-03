import time
from typing import Any, Dict, Tuple

class WeatherCache:
    """Простой in-memory кэш с TTL."""
    def __init__(self, ttl_seconds: int = 300) -> None:
        self._ttl = ttl_seconds
        self._store: Dict[Tuple, Tuple[float, Any]] = {}

    def get(self, key: Tuple) -> Any | None:
        item = self._store.get(key)
        if not item:
            return None
        ts, value = item
        if time.time() - ts > self._ttl:
            self._store.pop(key, None)
            return None
        return value

    def set(self, key: Tuple, value: Any) -> None:
        self._store[key] = (time.time(), value)


class UserUnitsStore:
    """Хранение выбранных единиц измерения на пользователя."""
    def __init__(self, default_units: str = "metric") -> None:
        self._default = default_units
        self._store: Dict[int, str] = {}

    def set_units(self, user_id: int, units: str) -> None:
        if units not in ("metric", "imperial"):
            units = self._default
        self._store[user_id] = units

    def get_units(self, user_id: int) -> str:
        return self._store.get(user_id, self._default)
