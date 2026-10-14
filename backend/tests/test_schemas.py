"""Tests for Pydantic schemas."""
import pytest
from pydantic import ValidationError

from landslide_backend.models.enums import RiskTier, ResourceType, ShelterStatus
from landslide_backend.models.schemas import (
    RiskZoneCreate,
    ResourceCreate,
    ShelterCreate,
    PredictionRequest,
)


class TestRiskZoneSchemas:
    """Test risk zone schemas."""
    
    def test_valid_risk_zone(self):
        """Test valid risk zone creation."""
        data = {
            "grid_cell_id": "cell_001",
            "risk_tier": RiskTier.WATCH,
            "confidence": 0.85,
            "model_version": "0.1.0",
        }
        zone = RiskZoneCreate(**data)
        assert zone.grid_cell_id == "cell_001"
        assert zone.risk_tier == RiskTier.WATCH
        assert zone.confidence == 0.85
        assert zone.model_version == "0.1.0"
    
    def test_invalid_confidence_above_one(self):
        """Test that confidence > 1 fails validation."""
        with pytest.raises(ValidationError):
            RiskZoneCreate(
                grid_cell_id="cell_001",
                risk_tier=RiskTier.WATCH,
                confidence=1.5,
            )
    
    def test_invalid_confidence_negative(self):
        """Test that negative confidence fails validation."""
        with pytest.raises(ValidationError):
            RiskZoneCreate(
                grid_cell_id="cell_001",
                risk_tier=RiskTier.WATCH,
                confidence=-0.1,
            )
    
    def test_empty_grid_cell_id(self):
        """Test that empty grid cell ID fails validation."""
        with pytest.raises(ValidationError):
            RiskZoneCreate(
                grid_cell_id="",
                risk_tier=RiskTier.WATCH,
                confidence=0.5,
            )
    
    def test_valid_risk_tier_string(self):
        """Test that string risk tier works."""
        data = {
            "grid_cell_id": "cell_002",
            "risk_tier": "alert",
            "confidence": 0.9,
        }
        zone = RiskZoneCreate(**data)
        assert zone.risk_tier == RiskTier.ALERT
    
    def test_invalid_risk_tier(self):
        """Test that invalid risk tier fails."""
        with pytest.raises(ValidationError):
            RiskZoneCreate(
                grid_cell_id="cell_003",
                risk_tier="danger",  # Not a valid tier
                confidence=0.5,
            )
    
    @pytest.mark.parametrize("confidence", [0.0, 0.1, 0.5, 0.9, 1.0])
    def test_boundary_confidences(self, confidence):
        """Test valid confidence boundary values."""
        zone = RiskZoneCreate(
            grid_cell_id=f"cell_{confidence}",
            risk_tier=RiskTier.WATCH,
            confidence=confidence,
        )
        assert zone.confidence == confidence


class TestResourceSchemas:
    """Test resource schemas."""
    
    def test_valid_resource(self):
        """Test valid resource creation."""
        data = {
            "name": "Ambulance Unit 1",
            "resource_type": ResourceType.MEDICAL,
            "capacity": 10,
            "location": {"lat": 28.6139, "lon": 77.2090},
        }
        resource = ResourceCreate(**data)
        assert resource.name == "Ambulance Unit 1"
        assert resource.resource_type == ResourceType.MEDICAL
        assert resource.capacity == 10
    
    def test_invalid_latitude(self):
        """Test invalid latitude fails."""
        with pytest.raises(ValidationError):
            ResourceCreate(
                name="Test Resource",
                resource_type=ResourceType.MEDICAL,
                capacity=10,
                location={"lat": 91, "lon": 77.2090},
            )
    
    def test_invalid_longitude(self):
        """Test invalid longitude fails."""
        with pytest.raises(ValidationError):
            ResourceCreate(
                name="Test Resource",
                resource_type=ResourceType.MEDICAL,
                capacity=10,
                location={"lat": 28.6139, "lon": 181},
            )
    
    def test_negative_capacity(self):
        """Test negative capacity fails."""
        with pytest.raises(ValidationError):
            ResourceCreate(
                name="Test Resource",
                resource_type=ResourceType.MEDICAL,
                capacity=-1,
                location={"lat": 28.6139, "lon": 77.2090},
            )
    
    def test_missing_location_coordinates(self):
        """Test missing coordinates fails."""
        with pytest.raises(ValidationError):
            ResourceCreate(
                name="Test Resource",
                resource_type=ResourceType.MEDICAL,
                capacity=10,
                location={"lat": 28.6139},
            )


class TestShelterSchemas:
    """Test shelter schemas."""
    
    def test_valid_shelter(self):
        """Test valid shelter creation."""
        data = {
            "name": "Community Center",
            "capacity": 100,
            "current_occupancy": 50,
            "location": {"lat": 28.6139, "lon": 77.2090},
            "status": ShelterStatus.OPEN,
        }
        shelter = ShelterCreate(**data)
        assert shelter.name == "Community Center"
        assert shelter.current_occupancy == 50
        assert shelter.status == ShelterStatus.OPEN
    
    def test_occupancy_exceeds_capacity(self):
        """Test occupancy > capacity fails."""
        with pytest.raises(ValidationError):
            ShelterCreate(
                name="Test Shelter",
                capacity=50,
                current_occupancy=75,
                location={"lat": 28.6139, "lon": 77.2090},
            )
    
    def test_valid_full_shelter(self):
        """Test that occupancy == capacity is valid."""
        data = {
            "name": "Full Shelter",
            "capacity": 50,
            "current_occupancy": 50,
            "location": {"lat": 28.6139, "lon": 77.2090},
        }
        shelter = ShelterCreate(**data)
        assert shelter.current_occupancy == shelter.capacity
    
    def test_default_occupancy(self):
        """Test default occupancy is 0."""
        data = {
            "name": "Empty Shelter",
            "capacity": 100,
            "location": {"lat": 28.6139, "lon": 77.2090},
        }
        shelter = ShelterCreate(**data)
        assert shelter.current_occupancy == 0


class TestPredictionSchemas:
    """Test prediction schemas."""
    
    def test_valid_prediction_request(self):
        """Test valid prediction request."""
        data = {
            "grid_cell_id": "cell_001",
            "recent_rainfall": [0.5, 1.2, 3.4, 2.1],
        }
        request = PredictionRequest(**data)
        assert request.grid_cell_id == "cell_001"
        assert len(request.recent_rainfall) == 4
    
    def test_empty_rainfall(self):
        """Test empty rainfall list fails."""
        with pytest.raises(ValidationError):
            PredictionRequest(
                grid_cell_id="cell_001",
                recent_rainfall=[],
            )
    
    def test_negative_rainfall(self):
        """Test negative rainfall fails."""
        with pytest.raises(ValidationError):
            PredictionRequest(
                grid_cell_id="cell_001",
                recent_rainfall=[0.5, -1.0, 2.0],
            )
