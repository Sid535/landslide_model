"""Service for risk assessment business logic."""
from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from ..exceptions import ResourceNotFoundError, ValidationError
from ..models.db import RiskZone
from ..models.enums import RiskTier
from ..models.schemas import RiskZoneCreate, RiskZoneUpdate
from ..repositories.risk_zone_repo import RiskZoneRepository


class RiskService:
    """Service for managing risk zones."""
    
    def __init__(self, db: AsyncSession):
        self.repository = RiskZoneRepository(db)
    
    async def create_risk_zone(self, data: RiskZoneCreate) -> RiskZone:
        """Create a new risk zone."""
        # Check if grid cell already exists
        existing = await self.repository.get_by_grid_cell_id(data.grid_cell_id)
        if existing:
            raise ValidationError(
                f"Risk zone with grid_cell_id '{data.grid_cell_id}' already exists"
            )
        
        return await self.repository.create(**data.model_dump())
    
    async def get_risk_zone(self, zone_id: UUID) -> RiskZone:
        """Get risk zone by ID."""
        zone = await self.repository.get(zone_id)
        if not zone:
            raise ResourceNotFoundError("RiskZone", str(zone_id))
        return zone
    
    async def get_risk_zone_by_cell(self, grid_cell_id: str) -> RiskZone:
        """Get risk zone by grid cell ID."""
        zone = await self.repository.get_by_grid_cell_id(grid_cell_id)
        if not zone:
            raise ResourceNotFoundError("RiskZone", grid_cell_id)
        return zone
    
    async def get_all_risk_zones(
        self, skip: int = 0, limit: int = 100
    ) -> List[RiskZone]:
        """Get all risk zones with pagination."""
        return await self.repository.get_all(skip=skip, limit=limit)
    
    async def get_zones_by_tier(self, tier: RiskTier) -> List[RiskZone]:
        """Get all risk zones with a specific tier."""
        return await self.repository.get_by_tier(tier)
    
    async def get_high_risk_zones(
        self, min_confidence: float = 0.7
    ) -> List[RiskZone]:
        """Get high-risk zones requiring attention."""
        return await self.repository.get_high_risk_zones(min_confidence)
    
    async def update_risk_zone(
        self, zone_id: UUID, data: RiskZoneUpdate
    ) -> RiskZone:
        """Update a risk zone."""
        zone = await self.get_risk_zone(zone_id)
        
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            raise ValidationError("No fields to update")
        
        updated = await self.repository.update(zone_id, **update_data)
        if not updated:
            raise ResourceNotFoundError("RiskZone", str(zone_id))
        
        return updated
    
    async def delete_risk_zone(self, zone_id: UUID) -> bool:
        """Delete a risk zone."""
        deleted = await self.repository.delete(zone_id)
        if not deleted:
            raise ResourceNotFoundError("RiskZone", str(zone_id))
        return True
    
    async def get_zones_by_model_version(
        self, version: str
    ) -> List[RiskZone]:
        """Get risk zones by model version."""
        return await self.repository.get_by_model_version(version)
    
    async def count_risk_zones(self) -> int:
        """Count total risk zones."""
        return await self.repository.count()
