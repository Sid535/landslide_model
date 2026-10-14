"""Service for shelter management business logic."""
from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from ..exceptions import ResourceNotFoundError, ValidationError
from ..models.db import Shelter
from ..models.enums import ShelterStatus
from ..models.schemas import ShelterCreate, ShelterUpdate
from ..repositories.shelter_repo import ShelterRepository


class ShelterService:
    """Service for managing shelters."""
    
    def __init__(self, db: AsyncSession):
        self.repository = ShelterRepository(db)
    
    async def create_shelter(self, data: ShelterCreate) -> Shelter:
        """Create a new shelter."""
        # Convert location dict to WKT
        data_dict = data.model_dump()
        data_dict["location"] = data.location_wkt
        
        return await self.repository.create(**data_dict)
    
    async def get_shelter(self, shelter_id: UUID) -> Shelter:
        """Get shelter by ID."""
        shelter = await self.repository.get(shelter_id)
        if not shelter:
            raise ResourceNotFoundError("Shelter", str(shelter_id))
        return shelter
    
    async def get_all_shelters(
        self, skip: int = 0, limit: int = 100
    ) -> List[Shelter]:
        """Get all shelters with pagination."""
        return await self.repository.get_all(skip=skip, limit=limit)
    
    async def get_open_shelters(self) -> List[Shelter]:
        """Get all open shelters."""
        return await self.repository.get_open_shelters()
    
    async def get_shelters_with_capacity(
        self, min_capacity: int = 1
    ) -> List[Shelter]:
        """Get shelters with available capacity."""
        return await self.repository.get_shelters_with_capacity(min_capacity)
    
    async def update_shelter(
        self, shelter_id: UUID, data: ShelterUpdate
    ) -> Shelter:
        """Update a shelter."""
        shelter = await self.get_shelter(shelter_id)
        
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            raise ValidationError("No fields to update")
        
        # Validate occupancy if updating
        if "current_occupancy" in update_data:
            new_occupancy = update_data["current_occupancy"]
            capacity = update_data.get("capacity", shelter.capacity)
            if new_occupancy > capacity:
                raise ValidationError(
                    f"Occupancy ({new_occupancy}) cannot exceed capacity ({capacity})"
                )
        
        updated = await self.repository.update(shelter_id, **update_data)
        if not updated:
            raise ResourceNotFoundError("Shelter", str(shelter_id))
        
        return updated
    
    async def update_shelter_occupancy(
        self, shelter_id: UUID, new_occupancy: int
    ) -> Shelter:
        """Update shelter occupancy."""
        updated = await self.repository.update_occupancy(
            shelter_id, new_occupancy
        )
        if not updated:
            shelter = await self.get_shelter(shelter_id)
            raise ValidationError(
                f"Invalid occupancy ({new_occupancy}) for shelter with "
                f"capacity {shelter.capacity}"
            )
        return updated
    
    async def delete_shelter(self, shelter_id: UUID) -> bool:
        """Delete a shelter."""
        deleted = await self.repository.delete(shelter_id)
        if not deleted:
            raise ResourceNotFoundError("Shelter", str(shelter_id))
        return True
    
    async def count_shelters(self) -> int:
        """Count total shelters."""
        return await self.repository.count()
