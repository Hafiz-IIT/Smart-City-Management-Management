# demo_data.py
import random
from datetime import datetime, timedelta
from app.core.models import Incident
from app.core.utils import uid, now_ms, latlng_to_ward
from app.services.store import write_incidents

WARDS = ["A", "B", "C"]
TYPES = ["pothole", "streetlight", "water-leak", "garbage"]
STATUS = ["open", "assigned", "resolved"]

def fake_incidents(n=20):
    items = []
    base_lat, base_lng = 22.56, 88.39
    for _ in range(n):
        lat = base_lat + (random.random() - 0.5) * 0.1
        lng = base_lng + (random.random() - 0.5) * 0.1
        t = random.choice(TYPES)
        desc = f"Demo {t} report"
        created = now_ms() - random.randint(0, 7*24*3600*1000)  # last 7 days
        status = random.choices(STATUS, weights=[0.4, 0.2, 0.4])[0]
        item = Incident(
            id=uid(),
            ward=latlng_to_ward(lat, lng),
            type=t,
            description=desc,
            lat=lat, lng=lng,
            createdAt=created,
            slaHours=random.choice([12,24,48]),
            status=status,
            assignedTo="Officer-"+str(random.randint(1,10)) if status!="open" else None
        )
        items.append(item)
    return items

if __name__ == "__main__":
    items = fake_incidents(25)
    write_incidents(items)
    print(f"Seeded {len(items)} demo incidents into app/data/incidents.json ✅")
