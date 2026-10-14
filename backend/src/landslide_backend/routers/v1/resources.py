"""Resource API endpoints."""
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...database import get_db
from ...models.enums import ResourceType
from ...models.schemas import (
    ResourceCreate,
    ResourceResponse,
    ResourceUpdate,
)
from ...services.resource_service import ResourceService

router = APIRouter()


@router.post(
    "/",
    response_model=ResourceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new resource",
)
async def create_resource(
    data: ResourceCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new emergency resource."""
    service = ResourceService(db)
    return await service.create_resource(data)


@router.get(
    "/",
    response_model=List[ResourceResponse],
    summary="Get all resources",
)
async def get_resources(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
):
    """Get all resources with pagination."""
    service = ResourceService(db)
    return await service.get_all_resources(skip=skip, limit=limit)


@router.get(
    "/available",
    response_model=List[ResourceResponse],
    summary="Get available resources",
)
async def get_available_resources(
    db: AsyncSession = Depends(get_db),
):
    """Get all available resources."""
    service = ResourceService(db)
    return await service.get_available_resources()


@router.get(
    "/type/{resource_type}",
    response_model=List[ResourceResponse],
    summary="Get resources by type",
)
async def get_resources_by_type(
    resource_type: ResourceType,
    db: AsyncSession = Depends(get_db),
):
    """Get resources of a specific type."""
    service = ResourceService(db)
    return await service.get_resources_by_type(resource_type)


@router.get(
    "/{resource_id}",
    response_model=ResourceResponse,
    summary="Get resource by ID",
)
async def get_resource(
    resource_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get a specific resource by its ID."""
    service = ResourceService(db)
    return await service.get_resource(resource_id)


@router.put(
    "/{resource_id}",
    response_model=ResourceResponse,
    summary="Update a resource",
)
async def update_resource(
    resource_id: UUID,
    data: ResourceUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update an existing resource."""
    service = ResourceService(db)
    return await service.update_resource(resource_id, data)


@router.delete(
    "/{resource_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a resource",
)
async def delete_resource(
    resource_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Delete a resource."""
    service = ResourceService(db)
    await service.delete_resource(resource_id)
