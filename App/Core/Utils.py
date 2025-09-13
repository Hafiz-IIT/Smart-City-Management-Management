# app/core/utils.py
import random
import time

def uid() -> str:
    return hex(int(time.time() * 1000))[2:] + str(random.randint(1000,9999))

def now_ms() -> int:
    return int(time.time() * 1000)

def latlng_to_ward(lat: float, lng: float) -> str:
    # toy partitioning for demo (Kolkata-ish box)
    if lng < 88.40 and lat >= 22.55:
        return 'A'
    if lng >= 88.40 and lat >= 22.55:
        return 'B'
    return 'C'
