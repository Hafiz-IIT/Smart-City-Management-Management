import secrets
import time
def uid() -> str:
    return secrets.token_urlsafe(18)
def now_ms() -> int:
    return int(time.time() * 1000)
def latlng_to_ward(lat: float, lng: float) -> str:
    # Demonstration-only partition; replace with authoritative ward boundaries.
    if lng < 88.40 and lat >= 22.55: return 'A'
    if lng >= 88.40 and lat >= 22.55: return 'B'
    return 'C'
