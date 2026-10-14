"""Tests for database models."""
import pytest

from landslide_backend.models.db import Resource, RiskZone, Shelter
from landslide_backend.models.enums import (
    ResourceStatus,
    ResourceType,
    RiskTier,
    ShelterStatus,
)


class TestRiskZoneModel:
    """Test RiskZone model."""
    
    def test_table_name(self):
        """Test table name is correct."""
        assert RiskZone.__tablename__ == "risk_zones"
    
    def test_required_columns(self):
        """Test required columns exist."""
        columns = [c.name for c in RiskZone.__table__.columns]
        required = [
            "id", "grid_cell_id", "risk_tier", "confidence",
            "geometry", "created_at", "updated_at"
        ]
        for col in required:
            assert col in columns, f"Missing column: {col}"
    
    def test_optional_columns(self):
        """Test optional columns exist."""
        columns = [c.name for c in RiskZone.__table__.columns]
        optional = ["rainfall_data", "model_version"]
        for col in optional:
            assert col in columns, f"Missing optional column: {col}"
    
    def test_unique_constraint(self):
        """Test grid_cell_id has unique constraint."""
        grid_cell_col = RiskZone.__table__.columns["grid_cell_id"]
        assert grid_cell_col.unique is True


class TestResourceModel:
    """Test Resource model."""
    
    def test_table_name(self):
        """Test table name is correct."""
        assert Resource.__tablename__ == "resources"
    
    def test_required_columns(self):
        """Test required columns exist."""
        columns = [c.name for c in Resource.__table__.columns]
        required = [
            "id", "name", "resource_type", "capacity",
            "location", "status", "created_at"
        ]
        for col in required:
            assert col in columns, f"Missing column: {col}"
    
    def test_optional_columns(self):
        """Test optional columns exist."""
        columns = [c.name for c in Resource.__table__.columns]
        assert "contact_info" in columns


class TestShelterModel:
    """Test Shelter model."""
    
    def test_table_name(self):
        """Test table name is correct."""
        assert Shelter.__tablename__ == "shelters"
    
    def test_required_columns(self):
        """Test required columns exist."""
        columns = [c.name for c in Shelter.__table__.columns]
        required = [
            "id", "name", "capacity", "current_occupancy",
            "location", "status", "created_at"
        ]
        for col in required:
            assert col in columns, f"Missing column: {col}"
    
    def test_optional_columns(self):
        """Test optional columns exist."""
        columns = [c.name for c in Shelter.__table__.columns]
        assert "facilities" in columns
