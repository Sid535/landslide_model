"""Tests for RiskService business logic."""
import pytest
from uuid import uuid4

from landslide_backend.exceptions import ResourceNotFoundError, ValidationError
from landslide_backend.models.enums import RiskTier
from landslide_backend.models.schemas import RiskZoneCreate, RiskZoneUpdate
from landslide_backend.services.risk_service import RiskService


class TestRiskService:
    """Test business logic in RiskService."""
    
    async def test_create_risk_zone(self, db_session):
        """Test creating a risk zone through service."""
        service = RiskService(db_session)
        
        data = RiskZoneCreate(
            grid_cell_id="service_test_001",
            risk_tier=RiskTier.WATCH,
            confidence=0.85,
            geometry="POLYGON((77.0 28.0, 77.1 28.0, 77.1 28.1, 77.0 28.1, 77.0 28.0))",
        )
        
        zone = await service.create_risk_zone(data)
        assert zone.grid_cell_id == "service_test_001"
        assert zone.risk_tier == RiskTier.WATCH
    
    async def test_create_duplicate_grid_cell(self, db_session):
        """Test creating duplicate grid cell raises validation error."""
        service = RiskService(db_session)
        
        data1 = RiskZoneCreate(
            grid_cell_id="service_test_002",
            risk_tier=RiskTier.WATCH,
            confidence=0.8,
            geometry="POLYGON((77.0 28.0, 77.1 28.0, 77.1 28.1, 77.0 28.1, 77.0 28.0))",
        )
        await service.create_risk_zone(data1)
        
        # Try to create duplicate
        data2 = RiskZoneCreate(
            grid_cell_id="service_test_002",  # Same ID
            risk_tier=RiskTier.ALERT,
            confidence=0.9,
            geometry="POLYGON((77.0 28.0, 77.1 28.0, 77.1 28.1, 77.0 28.1, 77.0 28.0))",
        )
        
        with pytest.raises(ValidationError):
            await service.create_risk_zone(data2)
    
    async def test_get_nonexistent_zone(self, db_session):
        """Test getting non-existent zone raises ResourceNotFoundError."""
        service = RiskService(db_session)
        
        with pytest.raises(ResourceNotFoundError):
            await service.get_risk_zone(uuid4())
    
    async def test_update_zone(self, db_session):
        """Test updating a zone through service."""
        service = RiskService(db_session)
        
        # Create
        data = RiskZoneCreate(
            grid_cell_id="service_test_003",
            risk_tier=RiskTier.WATCH,
            confidence=0.7,
            geometry="POLYGON((77.0 28.0, 77.1 28.0, 77.1 28.1, 77.0 28.1, 77.0 28.0))",
        )
        zone = await service.create_risk_zone(data)
        
        # Update
        update_data = RiskZoneUpdate(risk_tier=RiskTier.EVACUATE, confidence=0.95)
        updated = await service.update_risk_zone(zone.id, update_data)
        
        assert updated.risk_tier == RiskTier.EVACUATE
        assert updated.confidence == 0.95
    
    async def test_delete_zone(self, db_session):
        """Test deleting a zone through service."""
        service = RiskService(db_session)
        
        # Create
        data = RiskZoneCreate(
            grid_cell_id="service_test_004",
            risk_tier=RiskTier.WATCH,
            confidence=0.7,
            geometry="POLYGON((77.0 28.0, 77.1 28.0, 77.1 28.1, 77.0 28.1, 77.0 28.0))",
        )
        zone = await service.create_risk_zone(data)
        
        # Delete
        deleted = await service.delete_risk_zone(zone.id)
        assert deleted is True
        
        # Verify deletion
        with pytest.raises(ResourceNotFoundError):
            await service.get_risk_zone(zone.id)
    
    async def test_get_zones_by_tier(self, db_session):
        """Test filtering zones by tier."""
        service = RiskService(db_session)
        
        # Create zones with different tiers
        data1 = RiskZoneCreate(
            grid_cell_id="service_test_005",
            risk_tier=RiskTier.WATCH,
            confidence=0.7,
            geometry="POLYGON((77.0 28.0, 77.1 28.0, 77.1 28.1, 77.0 28.1, 77.0 28.0))",
        )
        await service.create_risk_zone(data1)
        
        data2 = RiskZoneCreate(
            grid_cell_id="service_test_006",
            risk_tier=RiskTier.ALERT,
            confidence=0.8,
            geometry="POLYGON((78.0 29.0, 78.1 29.0, 78.1 29.1, 78.0 29.1, 78.0 29.0))",
        )
        await service.create_risk_zone(data2)
        
        alert_zones = await service.get_zones_by_tier(RiskTier.ALERT)
        assert len(alert_zones) == 1
        assert alert_zones[0].grid_cell_id == "service_test_006"
