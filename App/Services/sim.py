# app/services/sim.py
import random
import time
from typing import List
from app.core.models import SensorReading
from app.core.utils import latlng_to_ward

SENSOR_TYPES = ['traffic', 'aqi', 'waste', 'noise']

def _jitter(base: float, rng: float = 0.12) -> float:
    return base + (random.random() - 0.5) * rng

def generate_sensor_batch(n: int = 24) -> List[SensorReading]:
    base_lat, base_lng = 22.56, 88.39
    out = []
    now = int(time.time() * 1000)
    for i in range(n):
        lat = _jitter(base_lat)
        lng = _jitter(base_lng)
        t = SENSOR_TYPES[i % len(SENSOR_TYPES)]
        base = {'aqi': 60, 'traffic': 50, 'waste': 40, 'noise': 30}[t]
        value = round(base + random.random() * 40, 2)
        ward = latlng_to_ward(lat, lng)
        out.append(SensorReading(id=f"{t}-{i}-{now}", type=t, lat=lat, lng=lng, value=value, ward=ward, ts=now))
    return out

def predict_traffic_hotspots(k: int = 3):
    return [
        dict(id=f"t-{i}", lat=22.52 + random.random()*0.12, lng=88.34 + random.random()*0.12, congestion=int(60 + random.random()*40))
        for i in range(k)
    ]

def predict_bin_overflow(k: int = 4):
    return [
        dict(id=f"b-{i}", ward=random.choice(['A','B','C']), hours=int(3 + random.random()*20))
        for i in range(k)
    ]
