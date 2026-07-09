from pydantic import BaseModel
from typing import Optional


class PlaceCreate(BaseModel):
    name: str
    category: str
    visit_duration_minutes: int
    open_hour: Optional[str] = None
    close_hour: Optional[str] = None


class PlaceResponse(BaseModel):
    id: int
    name: str
    category: str
    visit_duration_minutes: int
    open_hour: Optional[str] = None
    close_hour: Optional[str] = None

    class Config:
        from_attributes = True

class CityRequest(BaseModel):
    city: str


class DiscoveredPlace(BaseModel):
    name: str
    category: str
    visit_duration_minutes: int
    lat: Optional[float] = None
    lon: Optional[float] = None


class DiscoveryResponse(BaseModel):
    city: str
    places: list[DiscoveredPlace]
    travel_matrix: Optional[list[list[Optional[float]]]] = None