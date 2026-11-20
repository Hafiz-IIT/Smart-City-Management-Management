from pydantic import BaseModel, Field, HttpUrl
from typing import Literal, Optional
Ward = Literal['A', 'B', 'C']
SensorType = Literal['traffic', 'aqi', 'waste', 'noise']
IncidentType = Literal['pothole', 'streetlight', 'water-leak', 'garbage']
IncidentStatus = Literal['open', 'assigned', 'resolved', 'expired']
class SensorReading(BaseModel):
    id: str
    type: SensorType
    lat: float = Field(ge=-90, le=90)
    lng: float = Field(ge=-180, le=180)
    value: float
    ward: Ward
    ts: int
class Incident(BaseModel):
    id: str
    ward: Ward
    type: IncidentType
    description: str = Field(min_length=3, max_length=2000)
    photoUrl: Optional[HttpUrl] = None
    lat: float = Field(ge=-90, le=90)
    lng: float = Field(ge=-180, le=180)
    createdAt: int
    slaHours: int = Field(default=24, ge=1, le=168)
    status: IncidentStatus = 'open'
    assignedTo: Optional[str] = Field(default=None, min_length=1, max_length=120)
class IncidentCreate(BaseModel):
    description: str = Field(min_length=3, max_length=2000)
    type: Optional[IncidentType] = None
    lat: float = Field(ge=-90, le=90)
    lng: float = Field(ge=-180, le=180)
    photoUrl: Optional[HttpUrl] = None
    slaHours: int = Field(default=24, ge=1, le=168)
class IncidentUpdate(BaseModel):
    status: Optional[IncidentStatus] = None
    assignedTo: Optional[str] = Field(default=None, min_length=1, max_length=120)
