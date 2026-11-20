import random
from App.Core.Models import Incident
from App.Core.Utils import uid, now_ms, latlng_to_ward
from App.Services.store import write_incidents
TYPES = ["pothole", "streetlight", "water-leak", "garbage"]
STATUS = ["open", "assigned", "resolved"]
def fake_incidents(n=20, seed=7):
    if isinstance(n, bool) or not isinstance(n, int) or n < 0 or n > 1000:
        raise ValueError("n must be an integer between 0 and 1000")
    rng = random.Random(seed)
    items = []
    base_lat, base_lng = 22.56, 88.39
    for _ in range(n):
        lat = base_lat + (rng.random() - 0.5) * 0.1
        lng = base_lng + (rng.random() - 0.5) * 0.1
        kind = rng.choice(TYPES)
        status = rng.choices(STATUS, weights=[0.4, 0.2, 0.4])[0]
        items.append(Incident(id=uid(), ward=latlng_to_ward(lat, lng), type=kind,
            description=f"Demo {kind} report", lat=lat, lng=lng,
            createdAt=now_ms() - rng.randint(0, 7 * 24 * 3600 * 1000),
            slaHours=rng.choice([12, 24, 48]), status=status,
            assignedTo=f"Officer-{rng.randint(1, 10)}" if status != "open" else None))
    return items
if __name__ == "__main__":
    seeded = fake_incidents(25)
    write_incidents(seeded)
    print(f"Seeded {len(seeded)} demo incidents into App/data/incidents.json")
