"""Shelter API endpoints."""
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...database import get_db
from ...models.schemas import (
    ShelterCreate,
    ShelterResponse,
    ShelterUpdate,
)
from ...services.shelter_service import ShelterService

router = APIRouter()


@router.post(
    "/",
    response_model=ShelterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new shelter",
)
async def create_shelter(
    data: ShelterCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new shelter."""
    service = ShelterService(db)
    return await service.create_shelter(data)


@router.get(
    "/",
    response_model=List[ShelterResponse],
    summary="Get all shelters",
)
async def get_shelters(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
):
    """Get all shelters with pagination."""
    service = ShelterService(db)
    return await service.get_all_shelters(skip=skip, limit=limit)


@router.get(
    "/open",
    response_model=List[ShelterResponse],
    summary="Get open shelters",
)
async def get_open_shelters(
    db: AsyncSession = Depends(get_db),
):
    """Get all open shelters."""
    service = ShelterService(db)
    return await service.get_open_shelters()


@router.get(
    "/with-capacity",
    response_model=List[ShelterResponse],
    summary="Get shelters with capacity",
)
async def get_shelters_with_capacity(
    min_capacity: int = Query(1, ge=1),
    db: AsyncSession = Depends(get_db),
):
    """Get shelters with available capacity."""
    service = ShelterService(db)
    return await service.get_shelters_with_capacity(min_capacity)


@router.get(
    "/{shelter_id}",
    response_model=ShelterResponse,
    summary="Get shelter by ID",
)
async def get_shelter(
    shelter_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get a specific shelter by its ID."""
    service = ShelterService(db)
    return await service.get_shelter(shelter_id)


@router.put(
    "/{shelter_id}",
    response_model=ShelterResponse,
    summary="Update a shelter",
)
async def update_shelter(
    shelter_id: UUID,
    data: ShelterUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update an existing shelter."""
    service = ShelterService(db)
    return await service.update_shelter(shelter_id, data)


@router.delete(
    "/{shelter_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a shelter",
)
async def delete_shelter(
    shelter_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Delete a shelter."""
    service = ShelterService(db)
    await service.delete_shelter(shelter_id)
