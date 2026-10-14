"""Integration tests for API endpoints."""
import pytest
from httpx import AsyncClient


class TestHealthEndpoints:
    """Test health check endpoints."""
    
    async def test_root(self, client: AsyncClient):
        """Test root endpoint."""
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
    
    async def test_health(self, client: AsyncClient):
        """Test health endpoint."""
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestRiskZoneAPI:
    """Test risk zone API endpoints."""
    
    async def test_create_risk_zone(self, client: AsyncClient):
        """Test creating a risk zone."""
        data = {
            "grid_cell_id": "cell_001",
            "risk_tier": "watch",
            "confidence": 0.85,
            "geometry": "POLYGON((77.0 28.0, 77.1 28.0, 77.1 28.1, 77.0 28.1, 77.0 28.0))"
        }
        response = await client.post("/api/v1/risk-zones/", json=data)
        assert response.status_code == 201
        response_data = response.json()
        assert response_data["grid_cell_id"] == "cell_001"
    
    async def test_get_risk_zones_empty(self, client: AsyncClient):
        """Test getting risk zones when empty."""
        response = await client.get("/api/v1/risk-zones/")
        assert response.status_code == 200


class TestResourceAPI:
    """Test resource API endpoints."""
    
    async def test_create_resource(self, client: AsyncClient):
        """Test creating a resource."""
        data = {
            "name": "Ambulance Unit 1",
            "resource_type": "medical",
            "capacity": 10,
            "location": {"lat": 28.6139, "lon": 77.2090},
        }
        response = await client.post("/api/v1/resources/", json=data)
        assert response.status_code == 201
        response_data = response.json()
        assert response_data["name"] == "Ambulance Unit 1"


class TestShelterAPI:
    """Test shelter API endpoints."""
    
    async def test_create_shelter(self, client: AsyncClient):
        """Test creating a shelter."""
        data = {
            "name": "Community Center",
            "capacity": 100,
            "current_occupancy": 0,
            "location": {"lat": 28.6139, "lon": 77.2090},
        }
        response = await client.post("/api/v1/shelters/", json=data)
        assert response.status_code == 201
        response_data = response.json()
        assert response_data["name"] == "Community Center"
