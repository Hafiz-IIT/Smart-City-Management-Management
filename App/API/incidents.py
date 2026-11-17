from fastapi import APIRouter, HTTPException, Depends
import re

from App.Core.Models import Incident, IncidentCreate, IncidentUpdate
from App.Core.Auth import require_admin
from App.Core.Utils import uid, now_ms, latlng_to_ward
from App.Services.store import read_incidents, write_incidents

router = APIRouter(prefix="/api/incidents", tags=["incidents"])


def classify(desc: str) -> str | None:
    text = desc.casefold()
    if re.search(r"(pothole|road|asphalt|crack)", text):
        return "pothole"
    if re.search(r"(street ?light|lamp|dark)", text):
        return "streetlight"
    if re.search(r"(leak|pipe|water|seep)", text):
        return "water-leak"
    if re.search(r"(garbage|bin|trash|waste)", text):
        return None
    return "garbage"


@router.get("", response_model=dict)
def list_items():
    return {"items": read_incidents()}


@router.post("", response_model=dict, status_code=201)
def create_item(payload: IncidentCreate):
    incident_type = payload.type or classify(payload.description)
    if incident_type is None:
        raise HTTPException(status_code=422, detail="Incident category is unclear; select one explicitly.")
    item = Incident(
        id=uid(),
        ward=latlng_to_ward(payload.lat, payload.lng),
        type=incident_type,
        description=payload.description,
        photoUrl=payload.photoUrl,
        lat=payload.lat,
        lng=payload.lng,
        createdAt=now_ms(),
        slaHours=payload.slaHours,
        status="open",
    )
    items = read_incidents()
    items.append(item)
    write_incidents(items)
    return {"ok": True, "item": item}


ALLOWED_STATUS_TRANSITIONS = {
    "open": {"assigned", "expired"},
    "assigned": {"open", "resolved", "expired"},
    "resolved": set(),
    "expired": set(),
}


@router.patch("/{incident_id}", response_model=dict, dependencies=[Depends(require_admin)])
def update_item(incident_id: str, payload: IncidentUpdate):
    items = read_incidents()
    try:
        idx = next(i for i, item in enumerate(items) if item.id == incident_id)
    except StopIteration:
        raise HTTPException(status_code=404, detail="Not found")
    data = items[idx].model_dump()
    if payload.status is not None and payload.status != data["status"]:
        if payload.status not in ALLOWED_STATUS_TRANSITIONS[data["status"]]:
            raise HTTPException(status_code=409, detail=f"Invalid status transition: {data['status']} -> {payload.status}")
        if payload.status == "assigned" and not (payload.assignedTo or data.get("assignedTo")):
            raise HTTPException(status_code=422, detail="assignedTo is required when assigning an incident")
        data["status"] = payload.status
    if payload.assignedTo is not None:
        if data["status"] != "assigned":
            raise HTTPException(status_code=409, detail="assignedTo can only be changed for an assigned incident")
        data["assignedTo"] = payload.assignedTo.strip()
    items[idx] = Incident(**data)
    write_incidents(items)
    return {"ok": True, "item": items[idx]}
