"""Pydantic schemas for API request/response validation."""
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from geoalchemy2 import WKBElement
from geoalchemy2.shape import to_shape
from shapely import to_wkt

from .enums import (
    FacilityType,
    ResourceStatus,
    ResourceType,
    RiskTier,
    ShelterStatus,
)


def wkb_to_wkt(value: Any) -> Optional[str]:
    """Convert WKBElement to WKT string."""
    if value is None:
        return None
    if isinstance(value, str):
        return value
    if hasattr(value, 'data'):
        shape = to_shape(value)
        return to_wkt(shape)
    return str(value)


def wkb_to_latlon(value: Any) -> Dict[str, float]:
    """Convert WKBElement to {lat, lon} dict."""
    if isinstance(value, dict):
        return value
    if hasattr(value, 'data'):
        point = to_shape(value)
        return {"lat": point.y, "lon": point.x}
    return {"lat": 0.0, "lon": 0.0}


# ============ CONTACT INFO SCHEMA ============

class ContactInfo(BaseModel):
    """Structured contact information."""
    
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    organization: Optional[str] = None
    notes: Optional[str] = None


# ============ FACILITIES SCHEMA ============

class ShelterFacilities(BaseModel):
    """Structured shelter facilities."""
    
    medical: bool = False
    food: bool = False
    water: bool = False
    sanitation: bool = False
    power: bool = False
    communication: bool = False
    accessibility: bool = False
    
    @property
    def available_facilities(self) -> List[str]:
        """Return list of available facility names."""
        facilities = []
        for facility in FacilityType:
            if getattr(self, facility.value):
                facilities.append(facility.value)
        return facilities


# ============ RISK ZONE SCHEMAS ============

class RiskZoneBase(BaseModel):
    """Base schema for risk zones."""
    
    grid_cell_id: str = Field(..., min_length=1, max_length=100)
    risk_tier: RiskTier
    confidence: float = Field(..., ge=0, le=1)
    geometry: Optional[str] = Field(None, description="WKT format geometry")
    rainfall_data: Optional[Dict[str, Any]] = None
    model_version: Optional[str] = None
    
    @field_validator("grid_cell_id")
    @classmethod
    def validate_grid_cell_id(cls, v: str) -> str:
        """Validate grid cell ID format."""
        if not v.strip():
            raise ValueError("grid_cell_id cannot be empty")
        return v.strip()


class RiskZoneCreate(RiskZoneBase):
    """Schema for creating a risk zone."""
    pass


class RiskZoneUpdate(BaseModel):
    """Schema for updating a risk zone."""
    
    risk_tier: Optional[RiskTier] = None
    confidence: Optional[float] = Field(None, ge=0, le=1)
    rainfall_data: Optional[Dict[str, Any]] = None
    model_version: Optional[str] = None


class RiskZoneResponse(BaseModel):
    """Schema for risk zone response."""
    
    id: UUID
    grid_cell_id: str
    risk_tier: RiskTier
    confidence: float
    geometry: Optional[str] = None
    rainfall_data: Optional[Dict[str, Any]] = None
    model_version: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}
    
    @model_validator(mode="before")
    @classmethod
    def convert_geometry(cls, data: Any) -> Any:
        """Convert WKB geometry to WKT string."""
        if isinstance(data, dict) and "geometry" in data:
            data["geometry"] = wkb_to_wkt(data["geometry"])
        elif hasattr(data, "geometry"):
            data_dict = data.__dict__.copy()
            data_dict["geometry"] = wkb_to_wkt(getattr(data, "geometry", None))
            return data_dict
        return data


# ============ RESOURCE SCHEMAS ============

class ResourceBase(BaseModel):
    """Base schema for resources."""
    
    name: str = Field(..., min_length=1, max_length=200)
    resource_type: ResourceType
    capacity: int = Field(..., ge=0)
    location: Dict[str, float] = Field(
        ...,
        description="Location as {lat: float, lon: float}",
    )
    status: ResourceStatus = ResourceStatus.AVAILABLE
    contact_info: Optional[ContactInfo] = None
    
    @field_validator("location")
    @classmethod
    def validate_location(cls, v: Dict[str, float]) -> Dict[str, float]:
        """Validate location coordinates."""
        if "lat" not in v or "lon" not in v:
            raise ValueError("Location must contain 'lat' and 'lon'")
        
        lat = v["lat"]
        lon = v["lon"]
        
        if not (-90 <= lat <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        if not (-180 <= lon <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        
        return v
    
    @property
    def location_wkt(self) -> str:
        """Convert location to WKT format."""
        return f"POINT({self.location['lon']} {self.location['lat']})"


class ResourceCreate(ResourceBase):
    """Schema for creating a resource."""
    pass


class ResourceUpdate(BaseModel):
    """Schema for updating a resource."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    capacity: Optional[int] = Field(None, ge=0)
    status: Optional[ResourceStatus] = None
    contact_info: Optional[ContactInfo] = None


class ResourceResponse(BaseModel):
    """Schema for resource response."""
    
    id: UUID
    name: str
    resource_type: ResourceType
    capacity: int
    location: Dict[str, float]
    status: ResourceStatus
    contact_info: Optional[ContactInfo] = None
    created_at: datetime
    
    model_config = {"from_attributes": True}
    
    @model_validator(mode="before")
    @classmethod
    def convert_location(cls, data: Any) -> Any:
        """Convert WKB location to {lat, lon} dict."""
        if isinstance(data, dict) and "location" in data:
            data["location"] = wkb_to_latlon(data["location"])
        elif hasattr(data, "location"):
            data_dict = data.__dict__.copy()
            data_dict["location"] = wkb_to_latlon(getattr(data, "location", None))
            return data_dict
        return data


# ============ SHELTER SCHEMAS ============

class ShelterBase(BaseModel):
    """Base schema for shelters."""
    
    name: str = Field(..., min_length=1, max_length=200)
    capacity: int = Field(..., ge=0)
    current_occupancy: int = Field(0, ge=0)
    location: Dict[str, float] = Field(
        ...,
        description="Location as {lat: float, lon: float}",
    )
    facilities: Optional[ShelterFacilities] = None
    status: ShelterStatus = ShelterStatus.OPEN
    
    @field_validator("location")
    @classmethod
    def validate_location(cls, v: Dict[str, float]) -> Dict[str, float]:
        """Validate location coordinates."""
        if "lat" not in v or "lon" not in v:
            raise ValueError("Location must contain 'lat' and 'lon'")
        
        lat = v["lat"]
        lon = v["lon"]
        
        if not (-90 <= lat <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        if not (-180 <= lon <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        
        return v
    
    @model_validator(mode="after")
    def validate_occupancy(self):
        """Validate occupancy doesn't exceed capacity."""
        if self.current_occupancy > self.capacity:
            raise ValueError("current_occupancy cannot exceed capacity")
        return self
    
    @property
    def location_wkt(self) -> str:
        """Convert location to WKT format."""
        return f"POINT({self.location['lon']} {self.location['lat']})"


class ShelterCreate(ShelterBase):
    """Schema for creating a shelter."""
    pass


class ShelterUpdate(BaseModel):
    """Schema for updating a shelter."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    capacity: Optional[int] = Field(None, ge=0)
    current_occupancy: Optional[int] = Field(None, ge=0)
    facilities: Optional[ShelterFacilities] = None
    status: Optional[ShelterStatus] = None


class ShelterResponse(BaseModel):
    """Schema for shelter response."""
    
    id: UUID
    name: str
    capacity: int
    current_occupancy: int
    location: Dict[str, float]
    facilities: Optional[ShelterFacilities] = None
    status: ShelterStatus
    created_at: datetime
    
    model_config = {"from_attributes": True}
    
    @model_validator(mode="before")
    @classmethod
    def convert_location(cls, data: Any) -> Any:
        """Convert WKB location to {lat, lon} dict."""
        if isinstance(data, dict) and "location" in data:
            data["location"] = wkb_to_latlon(data["location"])
        elif hasattr(data, "location"):
            data_dict = data.__dict__.copy()
            data_dict["location"] = wkb_to_latlon(getattr(data, "location", None))
            return data_dict
        return data


# ============ PREDICTION SCHEMAS ============

class PredictionRequest(BaseModel):
    """Schema for prediction requests."""
    
    grid_cell_id: str = Field(..., min_length=1)
    recent_rainfall: List[float] = Field(..., min_length=1)
    terrain_data: Optional[Dict[str, Any]] = None
    
    @field_validator("recent_rainfall")
    @classmethod
    def validate_rainfall(cls, v: List[float]) -> List[float]:
        """Validate rainfall data."""
        if any(r < 0 for r in v):
            raise ValueError("Rainfall values cannot be negative")
        return v


class PredictionResponse(BaseModel):
    """Schema for prediction responses."""
    
    grid_cell_id: str
    risk_tier: RiskTier
    confidence: float = Field(..., ge=0, le=1)
    timestamp: datetime
    model_version: str
