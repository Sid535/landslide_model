"""Service for resource management business logic."""
from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from ..exceptions import ResourceNotFoundError, ValidationError
from ..models.db import Resource
from ..models.enums import ResourceStatus, ResourceType
from ..models.schemas import ResourceCreate, ResourceUpdate
from ..repositories.resource_repo import ResourceRepository


class ResourceService:
    """Service for managing emergency resources."""
    
    def __init__(self, db: AsyncSession):
        self.repository = ResourceRepository(db)
    
    async def create_resource(self, data: ResourceCreate) -> Resource:
        """Create a new resource."""
        # Convert location dict to WKT
        data_dict = data.model_dump()
        data_dict["location"] = data.location_wkt
        
        return await self.repository.create(**data_dict)
    
    async def get_resource(self, resource_id: UUID) -> Resource:
        """Get resource by ID."""
        resource = await self.repository.get(resource_id)
        if not resource:
            raise ResourceNotFoundError("Resource", str(resource_id))
        return resource
    
    async def get_all_resources(
        self, skip: int = 0, limit: int = 100
    ) -> List[Resource]:
        """Get all resources with pagination."""
        return await self.repository.get_all(skip=skip, limit=limit)
    
    async def get_resources_by_type(
        self, resource_type: ResourceType
    ) -> List[Resource]:
        """Get resources by type."""
        return await self.repository.get_by_type(resource_type)
    
    async def get_available_resources(self) -> List[Resource]:
        """Get all available resources."""
        return await self.repository.get_available_resources()
    
    async def get_available_resources_by_type(
        self, resource_type: ResourceType
    ) -> List[Resource]:
        """Get available resources of a specific type."""
        return await self.repository.get_available_by_type(resource_type)
    
    async def update_resource(
        self, resource_id: UUID, data: ResourceUpdate
    ) -> Resource:
        """Update a resource."""
        resource = await self.get_resource(resource_id)
        
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            raise ValidationError("No fields to update")
        
        updated = await self.repository.update(resource_id, **update_data)
        if not updated:
            raise ResourceNotFoundError("Resource", str(resource_id))
        
        return updated
    
    async def update_resource_status(
        self, resource_id: UUID, status: ResourceStatus
    ) -> Resource:
        """Update resource status."""
        updated = await self.repository.update_status(resource_id, status)
        if not updated:
            raise ResourceNotFoundError("Resource", str(resource_id))
        return updated
    
    async def delete_resource(self, resource_id: UUID) -> bool:
        """Delete a resource."""
        deleted = await self.repository.delete(resource_id)
        if not deleted:
            raise ResourceNotFoundError("Resource", str(resource_id))
        return True
    
    async def count_resources(self) -> int:
        """Count total resources."""
        return await self.repository.count()
