import time

_cache: dict[str, dict] = {}


def get_cache(key: str) -> dict | list | None:
    if key not in _cache:
        return None

    entry = _cache[key]
    if time.time() - entry['timestamp'] > entry['ttl']:
        del _cache[key]
        return None

    return entry['value']


def set_cache(key: str, value: dict | list, ttl: int) -> None:
    _cache[key] = {
        'value': value,
        'timestamp': time.time(),
        'ttl': ttl,
    }


def clear_cache() -> None:
    _cache.clear()
