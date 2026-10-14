"""SQLAlchemy database models."""
import uuid
from datetime import datetime, UTC
from typing import Optional

from geoalchemy2 import Geometry
from sqlalchemy import (
    JSON,
    CheckConstraint,
    Column,
    DateTime,
    Enum as SQLAlchemyEnum,
    Float,
    Integer,
    String,
)
from sqlalchemy.dialects.postgresql import UUID

from ..database import Base
from .enums import (
    ResourceStatus,
    ResourceType,
    RiskTier,
    ShelterStatus,
)


def utcnow() -> datetime:
    """Return current UTC datetime."""
    return datetime.now(UTC)


class RiskZone(Base):
    """Areas with landslide risk assessment."""
    
    __tablename__ = "risk_zones"
    __table_args__ = (
        CheckConstraint(
            "confidence >= 0 AND confidence <= 1",
            name="ck_risk_zone_confidence_range",
        ),
    )
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    grid_cell_id = Column(
        String,
        unique=True,
        index=True,
        nullable=False,
        comment="Unique identifier for the grid cell",
    )
    risk_tier = Column(
        SQLAlchemyEnum(RiskTier, name="risk_tier_enum"),
        nullable=False,
        index=True,
        comment="Risk level: watch, alert, or evacuate",
    )
    confidence = Column(
        Float,
        nullable=False,
        comment="Model confidence score (0-1)",
    )
    geometry = Column(
        Geometry("POLYGON", srid=4326, spatial_index=False),
        nullable=False,
        comment="Geographic boundary of the risk zone",
    )
    rainfall_data = Column(
        JSON,
        nullable=True,
        comment="Recent rainfall data used for prediction",
    )
    model_version = Column(
        String,
        nullable=True,
        comment="Version of the ML model used",
    )
    created_at = Column(
        DateTime(timezone=True),
        default=utcnow,
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=utcnow,
        onupdate=utcnow,
        nullable=False,
    )


class Resource(Base):
    """Emergency resources for disaster response."""
    
    __tablename__ = "resources"
    __table_args__ = (
        CheckConstraint(
            "capacity >= 0",
            name="ck_resource_capacity_positive",
        ),
    )
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    name = Column(
        String,
        nullable=False,
        comment="Name of the resource",
    )
    resource_type = Column(
        SQLAlchemyEnum(ResourceType, name="resource_type_enum"),
        nullable=False,
        index=True,
        comment="Type of resource (medical, rescue, food, etc.)",
    )
    capacity = Column(
        Integer,
        nullable=False,
        comment="Total capacity or quantity available",
    )
    location = Column(
        Geometry("POINT", srid=4326, spatial_index=False),
        nullable=False,
        comment="Geographic location of the resource",
    )
    status = Column(
        SQLAlchemyEnum(ResourceStatus, name="resource_status_enum"),
        default=ResourceStatus.AVAILABLE,
        nullable=False,
        index=True,
        comment="Current status of the resource",
    )
    contact_info = Column(
        JSON,
        nullable=True,
        comment="Contact information for resource management",
    )
    created_at = Column(
        DateTime(timezone=True),
        default=utcnow,
        nullable=False,
    )


class Shelter(Base):
    """Evacuation shelters."""
    
    __tablename__ = "shelters"
    __table_args__ = (
        CheckConstraint(
            "capacity >= 0",
            name="ck_shelter_capacity_positive",
        ),
        CheckConstraint(
            "current_occupancy >= 0",
            name="ck_shelter_occupancy_positive",
        ),
        CheckConstraint(
            "current_occupancy <= capacity",
            name="ck_shelter_occupancy_not_exceed_capacity",
        ),
    )
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    name = Column(
        String,
        nullable=False,
        comment="Name of the shelter",
    )
    capacity = Column(
        Integer,
        nullable=False,
        comment="Maximum number of people the shelter can hold",
    )
    current_occupancy = Column(
        Integer,
        default=0,
        nullable=False,
        comment="Current number of people in the shelter",
    )
    location = Column(
        Geometry("POINT", srid=4326, spatial_index=False),
        nullable=False,
        comment="Geographic location of the shelter",
    )
    facilities = Column(
        JSON,
        nullable=True,
        comment="List of facilities available (medical, food, water, etc.)",
    )
    status = Column(
        SQLAlchemyEnum(ShelterStatus, name="shelter_status_enum"),
        default=ShelterStatus.OPEN,
        nullable=False,
        index=True,
        comment="Current status of the shelter",
    )
    created_at = Column(
        DateTime(timezone=True),
        default=utcnow,
        nullable=False,
    )
