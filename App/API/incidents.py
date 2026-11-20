from fastapi import APIRouter, Depends, HTTPException
import re
from App.Core.Models import Incident, IncidentCreate, IncidentUpdate
from App.Core.Utils import uid, now_ms, latlng_to_ward
from App.Services.store import read_incidents, mutate_incidents
from App.API.auth import require_admin
router = APIRouter(prefix="/api/incidents", tags=["incidents"])
def classify(desc: str) -> str:
    text = desc.lower()
    if re.search(r"(pothole|road|asphalt|crack)", text): return "pothole"
    if re.search(r"(street ?light|lamp|dark)", text): return "streetlight"
    if re.search(r"(leak|pipe|water|seep)", text): return "water-leak"
    if re.search(r"(garbage|bin|trash|waste)", text): return "garbage"
    return "garbage"
@router.get("", response_model=dict)
def list_items():
    return {"items": read_incidents()}
@router.post("", response_model=dict, status_code=201)
def create_item(payload: IncidentCreate):
    kind = payload.type or classify(payload.description)
    item = Incident(id=uid(), ward=latlng_to_ward(payload.lat, payload.lng), type=kind,
        description=payload.description, photoUrl=payload.photoUrl, lat=payload.lat, lng=payload.lng,
        createdAt=now_ms(), slaHours=payload.slaHours, status="open")
    mutate_incidents(lambda items: items.append(item))
    return {"ok": True, "item": item}
@router.patch("/{incident_id}", response_model=dict, dependencies=[Depends(require_admin)])
def update_item(incident_id: str, payload: IncidentUpdate):
    if not payload.model_fields_set:
        raise HTTPException(status_code=400, detail="At least one update field is required")
    def apply_update(items):
        idx = next((i for i, item in enumerate(items) if item.id == incident_id), None)
        if idx is None: raise HTTPException(status_code=404, detail="Not found")
        data = items[idx].model_dump()
        if "status" in payload.model_fields_set: data["status"] = payload.status
        if "assignedTo" in payload.model_fields_set: data["assignedTo"] = payload.assignedTo
        items[idx] = Incident(**data)
        return items[idx]
    updated = mutate_incidents(apply_update)
    return {"ok": True, "item": updated}
