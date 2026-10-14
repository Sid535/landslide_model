"""Version 1 API routes."""
from fastapi import APIRouter

from . import risk, resources, shelters

# Create main v1 router
router = APIRouter()

# Include sub-routers
router.include_router(risk.router, prefix="/risk-zones", tags=["Risk Zones"])
router.include_router(resources.router, prefix="/resources", tags=["Resources"])
router.include_router(shelters.router, prefix="/shelters", tags=["Shelters"])
