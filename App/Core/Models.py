# app/core/models.py
from pydantic import BaseModel, Field, HttpUrl, ConfigDict
from typing import Literal, Optional
from datetime import datetime

Ward = Literal['A', 'B', 'C']
SensorType = Literal['traffic', 'aqi', 'waste', 'noise']
IncidentType = Literal['pothole', 'streetlight', 'water-leak', 'garbage']
IncidentStatus = Literal['open', 'assigned', 'resolved', 'expired']

class SensorReading(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str = Field(min_length=1)
    type: SensorType
    lat: float = Field(ge=-90, le=90, allow_inf_nan=False)
    lng: float = Field(ge=-180, le=180, allow_inf_nan=False)
    value: float = Field(allow_inf_nan=False)
    ward: Ward
    ts: int = Field(gt=0)  # epoch ms

class Incident(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str = Field(min_length=1)
    ward: Ward
    type: IncidentType
    description: str = Field(min_length=3)
    photoUrl: Optional[HttpUrl] = None
    lat: float = Field(ge=-90, le=90, allow_inf_nan=False)
    lng: float = Field(ge=-180, le=180, allow_inf_nan=False)
    createdAt: int = Field(gt=0)
    slaHours: int = Field(default=24, ge=1, le=168)
    status: IncidentStatus = 'open'
    assignedTo: Optional[str] = None

class IncidentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    description: str = Field(min_length=3)
    type: Optional[IncidentType] = None
    lat: float = Field(ge=-90, le=90, allow_inf_nan=False)
    lng: float = Field(ge=-180, le=180, allow_inf_nan=False)
    photoUrl: Optional[HttpUrl] = None
    slaHours: int = Field(default=24, ge=1, le=168)

class IncidentUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    status: Optional[IncidentStatus] = None
    assignedTo: Optional[str] = Field(default=None, min_length=1)
