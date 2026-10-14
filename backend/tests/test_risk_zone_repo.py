"""Tests for RiskZone repository - tests actual database operations."""
import pytest
from uuid import uuid4

from landslide_backend.models.enums import RiskTier
from landslide_backend.repositories.risk_zone_repo import RiskZoneRepository


class TestRiskZoneRepository:
    """Test actual CRUD operations against PostgreSQL."""
    
    async def test_create_and_retrieve(self, db_session):
        """Test creating and retrieving a risk zone."""
        repo = RiskZoneRepository(db_session)
        
        # Create
        zone = await repo.create(
            grid_cell_id="test_cell_001",
            risk_tier=RiskTier.WATCH,
            confidence=0.85,
            geometry="POLYGON((77.0 28.0, 77.1 28.0, 77.1 28.1, 77.0 28.1, 77.0 28.0))",
        )
        
        assert zone.id is not None
        assert zone.grid_cell_id == "test_cell_001"
        
        # Retrieve
        retrieved = await repo.get(zone.id)
        assert retrieved is not None
        assert retrieved.grid_cell_id == "test_cell_001"
        assert retrieved.risk_tier == RiskTier.WATCH
    
    async def test_unique_constraint_enforced(self, db_session):
        """Test that duplicate grid_cell_id raises an error."""
        repo = RiskZoneRepository(db_session)
        
        # Create first zone
        await repo.create(
            grid_cell_id="test_cell_002",
            risk_tier=RiskTier.WATCH,
            confidence=0.85,
            geometry="POLYGON((77.0 28.0, 77.1 28.0, 77.1 28.1, 77.0 28.1, 77.0 28.0))",
        )
        
        # Try to create duplicate
        with pytest.raises(Exception):
            await repo.create(
                grid_cell_id="test_cell_002",  # Duplicate
                risk_tier=RiskTier.ALERT,
                confidence=0.9,
                geometry="POLYGON((77.0 28.0, 77.1 28.0, 77.1 28.1, 77.0 28.1, 77.0 28.0))",
            )
    
    async def test_get_by_grid_cell_id(self, db_session):
        """Test retrieving by grid cell ID."""
        repo = RiskZoneRepository(db_session)
        
        await repo.create(
            grid_cell_id="test_cell_003",
            risk_tier=RiskTier.ALERT,
            confidence=0.9,
            geometry="POLYGON((77.0 28.0, 77.1 28.0, 77.1 28.1, 77.0 28.1, 77.0 28.0))",
        )
        
        retrieved = await repo.get_by_grid_cell_id("test_cell_003")
        assert retrieved is not None
        assert retrieved.risk_tier == RiskTier.ALERT
    
    async def test_get_by_tier(self, db_session):
        """Test retrieving by risk tier."""
        repo = RiskZoneRepository(db_session)
        
        # Create zones with different tiers
        await repo.create(
            grid_cell_id="test_cell_004",
            risk_tier=RiskTier.WATCH,
            confidence=0.7,
            geometry="POLYGON((77.0 28.0, 77.1 28.0, 77.1 28.1, 77.0 28.1, 77.0 28.0))",
        )
        await repo.create(
            grid_cell_id="test_cell_005",
            risk_tier=RiskTier.EVACUATE,
            confidence=0.95,
            geometry="POLYGON((78.0 29.0, 78.1 29.0, 78.1 29.1, 78.0 29.1, 78.0 29.0))",
        )
        
        evacuate_zones = await repo.get_by_tier(RiskTier.EVACUATE)
        assert len(evacuate_zones) == 1
        assert evacuate_zones[0].grid_cell_id == "test_cell_005"
    
    async def test_get_high_risk_zones(self, db_session):
        """Test retrieving high-risk zones."""
        repo = RiskZoneRepository(db_session)
        
        # Create zones with different confidence levels
        await repo.create(
            grid_cell_id="test_cell_006",
            risk_tier=RiskTier.ALERT,
            confidence=0.95,  # High confidence
            geometry="POLYGON((77.0 28.0, 77.1 28.0, 77.1 28.1, 77.0 28.1, 77.0 28.0))",
        )
        await repo.create(
            grid_cell_id="test_cell_007",
            risk_tier=RiskTier.ALERT,
            confidence=0.5,  # Low confidence
            geometry="POLYGON((78.0 29.0, 78.1 29.0, 78.1 29.1, 78.0 29.1, 78.0 29.0))",
        )
        
        high_risk = await repo.get_high_risk_zones(min_confidence=0.7)
        assert len(high_risk) == 1
        assert high_risk[0].grid_cell_id == "test_cell_006"
    
    async def test_update(self, db_session):
        """Test updating a risk zone."""
        repo = RiskZoneRepository(db_session)
        
        # Create
        zone = await repo.create(
            grid_cell_id="test_cell_008",
            risk_tier=RiskTier.WATCH,
            confidence=0.6,
            geometry="POLYGON((77.0 28.0, 77.1 28.0, 77.1 28.1, 77.0 28.1, 77.0 28.0))",
        )
        
        # Update
        updated = await repo.update(zone.id, risk_tier=RiskTier.ALERT, confidence=0.8)
        assert updated is not None
        assert updated.risk_tier == RiskTier.ALERT
        assert updated.confidence == 0.8
    
    async def test_delete(self, db_session):
        """Test deleting a risk zone."""
        repo = RiskZoneRepository(db_session)
        
        # Create
        zone = await repo.create(
            grid_cell_id="test_cell_009",
            risk_tier=RiskTier.WATCH,
            confidence=0.7,
            geometry="POLYGON((77.0 28.0, 77.1 28.0, 77.1 28.1, 77.0 28.1, 77.0 28.0))",
        )
        
        # Delete
        deleted = await repo.delete(zone.id)
        assert deleted is True
        
        # Verify deletion
        retrieved = await repo.get(zone.id)
        assert retrieved is None
    
    async def test_get_nonexistent(self, db_session):
        """Test retrieving non-existent zone returns None."""
        repo = RiskZoneRepository(db_session)
        
        retrieved = await repo.get(uuid4())
        assert retrieved is None
