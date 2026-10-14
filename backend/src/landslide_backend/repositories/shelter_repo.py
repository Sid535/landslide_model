"""Repository for Shelter model."""
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.db import Shelter
from ..models.enums import ShelterStatus
from .base_repo import BaseRepository


class ShelterRepository(BaseRepository[Shelter]):
    """Repository for shelter operations."""
    
    def __init__(self, db: AsyncSession):
        super().__init__(Shelter, db)
    
    async def get_open_shelters(self) -> List[Shelter]:
        """Get all open shelters."""
        result = await self.db.execute(
            select(Shelter).where(Shelter.status == ShelterStatus.OPEN)
        )
        return list(result.scalars().all())
    
    async def get_shelters_with_capacity(
        self, min_capacity: int = 1
    ) -> List[Shelter]:
        """Get shelters that have available capacity."""
        result = await self.db.execute(
            select(Shelter).where(
                Shelter.status == ShelterStatus.OPEN,
                Shelter.current_occupancy + min_capacity <= Shelter.capacity,
            )
        )
        return list(result.scalars().all())
    
    async def update_occupancy(
        self, shelter_id: UUID, new_occupancy: int
    ) -> Optional[Shelter]:
        """Update shelter occupancy."""
        shelter = await self.get(shelter_id)
        if shelter and 0 <= new_occupancy <= shelter.capacity:
            return await self.update(shelter_id, current_occupancy=new_occupancy)
        return None
    
    async def get_full_shelters(self) -> List[Shelter]:
        """Get shelters that are at full capacity."""
        result = await self.db.execute(
            select(Shelter).where(
                Shelter.current_occupancy >= Shelter.capacity,
                Shelter.status != ShelterStatus.CLOSED,
            )
        )
        return list(result.scalars().all())
