# app/core/utils.py
import time
import uuid

def uid() -> str:
    return uuid.uuid4().hex

def now_ms() -> int:
    return int(time.time() * 1000)

def latlng_to_ward(lat: float, lng: float) -> str:
    # toy partitioning for demo (Kolkata-ish box)
    if lng < 88.40 and lat >= 22.55:
        return 'A'
    if lng >= 88.40 and lat >= 22.55:
        return 'B'
    return 'C'
