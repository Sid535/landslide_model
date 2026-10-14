"""Repository for RiskZone model."""
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.db import RiskZone
from ..models.enums import RiskTier
from .base_repo import BaseRepository


class RiskZoneRepository(BaseRepository[RiskZone]):
    """Repository for risk zone operations."""
    
    def __init__(self, db: AsyncSession):
        super().__init__(RiskZone, db)
    
    async def get_by_grid_cell_id(self, grid_cell_id: str) -> Optional[RiskZone]:
        """Get risk zone by grid cell ID."""
        result = await self.db.execute(
            select(RiskZone).where(RiskZone.grid_cell_id == grid_cell_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_tier(self, tier: RiskTier) -> List[RiskZone]:
        """Get all risk zones with a specific tier."""
        result = await self.db.execute(
            select(RiskZone).where(RiskZone.risk_tier == tier)
        )
        return list(result.scalars().all())
    
    async def get_high_risk_zones(self, min_confidence: float = 0.7) -> List[RiskZone]:
        """Get zones with high confidence and risk level."""
        result = await self.db.execute(
            select(RiskZone)
            .where(
                RiskZone.risk_tier.in_([RiskTier.ALERT, RiskTier.EVACUATE]),
                RiskZone.confidence >= min_confidence,
            )
        )
        return list(result.scalars().all())
    
    async def get_by_model_version(self, version: str) -> List[RiskZone]:
        """Get risk zones predicted by a specific model version."""
        result = await self.db.execute(
            select(RiskZone).where(RiskZone.model_version == version)
        )
        return list(result.scalars().all())
