"""Repository for Resource model."""
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.db import Resource
from ..models.enums import ResourceStatus, ResourceType
from .base_repo import BaseRepository


class ResourceRepository(BaseRepository[Resource]):
    """Repository for resource operations."""
    
    def __init__(self, db: AsyncSession):
        super().__init__(Resource, db)
    
    async def get_by_type(self, resource_type: ResourceType) -> List[Resource]:
        """Get all resources of a specific type."""
        result = await self.db.execute(
            select(Resource).where(Resource.resource_type == resource_type)
        )
        return list(result.scalars().all())
    
    async def get_available_resources(self) -> List[Resource]:
        """Get all available resources."""
        result = await self.db.execute(
            select(Resource).where(Resource.status == ResourceStatus.AVAILABLE)
        )
        return list(result.scalars().all())
    
    async def get_resources_by_status(
        self, status: ResourceStatus
    ) -> List[Resource]:
        """Get resources by status."""
        result = await self.db.execute(
            select(Resource).where(Resource.status == status)
        )
        return list(result.scalars().all())
    
    async def update_status(
        self, resource_id: UUID, status: ResourceStatus
    ) -> Optional[Resource]:
        """Update resource status."""
        return await self.update(resource_id, status=status)
    
    async def get_available_by_type(
        self, resource_type: ResourceType
    ) -> List[Resource]:
        """Get available resources of a specific type."""
        result = await self.db.execute(
            select(Resource).where(
                Resource.resource_type == resource_type,
                Resource.status == ResourceStatus.AVAILABLE,
            )
        )
        return list(result.scalars().all())
