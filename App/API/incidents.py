# app/api/incidents.py
from fastapi import APIRouter, HTTPException
from typing import List
import re

from app.core.models import Incident, IncidentCreate, IncidentUpdate
from app.core.utils import uid, now_ms, latlng_to_ward
from app.services.store import read_incidents, write_incidents

router = APIRouter(prefix="/api/incidents", tags=["incidents"])

def classify(desc: str) -> str:
    t = desc.lower()
    if re.search(r"(pothole|road|asphalt|crack)", t): return "pothole"
    if re.search(r"(street ?light|lamp|dark)", t): return "streetlight"
    if re.search(r"(leak|pipe|water|seep)", t): return "water-leak"
    if re.search(r"(garbage|bin|trash|waste)", t): return "garbage"
    return "garbage"

@router.get("", response_model=dict)
def list_items():
    items = read_incidents()
    return {"items": items}

@router.post("", response_model=dict, status_code=201)
def create_item(payload: IncidentCreate):
    t = payload.type or classify(payload.description)
    item = Incident(
        id=uid(),
        ward=latlng_to_ward(payload.lat, payload.lng),
        type=t, description=payload.description,
        photoUrl=payload.photoUrl,
        lat=payload.lat, lng=payload.lng,
        createdAt=now_ms(), slaHours=payload.slaHours, status="open"
    )
    items = read_incidents()
    items.append(item)
    write_incidents(items)
    return {"ok": True, "item": item}

@router.patch("/{incident_id}", response_model=dict)
def update_item(incident_id: str, payload: IncidentUpdate):
    items = read_incidents()
    try:
        idx = next(i for i, it in enumerate(items) if it.id == incident_id)
    except StopIteration:
        raise HTTPException(status_code=404, detail="Not found")
    data = items[idx].model_dump()
    if payload.status is not None:
        data["status"] = payload.status
    if payload.assignedTo is not None:
        data["assignedTo"] = payload.assignedTo
    items[idx] = Incident(**data)
    write_incidents(items)
    return {"ok": True, "item": items[idx]}
