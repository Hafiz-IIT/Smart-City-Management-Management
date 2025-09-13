# app/core/models.py
from pydantic import BaseModel, Field, HttpUrl
from typing import Literal, Optional
from datetime import datetime

Ward = Literal['A', 'B', 'C']
SensorType = Literal['traffic', 'aqi', 'waste', 'noise']
IncidentType = Literal['pothole', 'streetlight', 'water-leak', 'garbage']
IncidentStatus = Literal['open', 'assigned', 'resolved', 'expired']

class SensorReading(BaseModel):
    id: str
    type: SensorType
    lat: float
    lng: float
    value: float
    ward: Ward
    ts: int  # epoch ms

class Incident(BaseModel):
    id: str
    ward: Ward
    type: IncidentType
    description: str
    photoUrl: Optional[HttpUrl] = None
    lat: float
    lng: float
    createdAt: int
    slaHours: int = 24
    status: IncidentStatus = 'open'
    assignedTo: Optional[str] = None

class IncidentCreate(BaseModel):
    description: str = Field(min_length=3)
    type: Optional[IncidentType] = None
    lat: float
    lng: float
    photoUrl: Optional[HttpUrl] = None
    slaHours: int = Field(default=24, ge=1, le=168)

class IncidentUpdate(BaseModel):
    status: Optional[IncidentStatus] = None
    assignedTo: Optional[str] = None
