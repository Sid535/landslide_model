"""Risk zone API endpoints."""
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...database import get_db
from ...models.enums import RiskTier
from ...models.schemas import (
    RiskZoneCreate,
    RiskZoneResponse,
    RiskZoneUpdate,
)
from ...services.risk_service import RiskService

router = APIRouter()


@router.post(
    "/",
    response_model=RiskZoneResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new risk zone",
)
async def create_risk_zone(
    data: RiskZoneCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new risk zone with the given data."""
    service = RiskService(db)
    return await service.create_risk_zone(data)


@router.get(
    "/",
    response_model=List[RiskZoneResponse],
    summary="Get all risk zones",
)
async def get_risk_zones(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
):
    """Get all risk zones with pagination."""
    service = RiskService(db)
    return await service.get_all_risk_zones(skip=skip, limit=limit)


@router.get(
    "/high-risk",
    response_model=List[RiskZoneResponse],
    summary="Get high-risk zones",
)
async def get_high_risk_zones(
    min_confidence: float = Query(0.7, ge=0, le=1),
    db: AsyncSession = Depends(get_db),
):
    """Get zones with high risk requiring attention."""
    service = RiskService(db)
    return await service.get_high_risk_zones(min_confidence)


@router.get(
    "/tier/{tier}",
    response_model=List[RiskZoneResponse],
    summary="Get risk zones by tier",
)
async def get_zones_by_tier(
    tier: RiskTier,
    db: AsyncSession = Depends(get_db),
):
    """Get all risk zones with a specific tier."""
    service = RiskService(db)
    return await service.get_zones_by_tier(tier)


@router.get(
    "/{zone_id}",
    response_model=RiskZoneResponse,
    summary="Get risk zone by ID",
)
async def get_risk_zone(
    zone_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get a specific risk zone by its ID."""
    service = RiskService(db)
    return await service.get_risk_zone(zone_id)


@router.put(
    "/{zone_id}",
    response_model=RiskZoneResponse,
    summary="Update a risk zone",
)
async def update_risk_zone(
    zone_id: UUID,
    data: RiskZoneUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update an existing risk zone."""
    service = RiskService(db)
    return await service.update_risk_zone(zone_id, data)


@router.delete(
    "/{zone_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a risk zone",
)
async def delete_risk_zone(
    zone_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Delete a risk zone."""
    service = RiskService(db)
    await service.delete_risk_zone(zone_id)
