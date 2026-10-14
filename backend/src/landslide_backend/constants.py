"""Application constants and configuration values."""

class APIConstants:
    """API-related constants."""
    VERSION = "v1"
    TITLE = "Landslide Risk Assessment API"
    DESCRIPTION = "Backend for landslide risk prediction and resource allocation"
    DEFAULT_PAGE_SIZE = 50
    MAX_PAGE_SIZE = 100

class GeoConstants:
    """Geospatial constants."""
    SRID = 4326  # WGS84 coordinate system
    INDIA_BBOX = {
        "min_lon": 68.7,
        "min_lat": 6.7,
        "max_lon": 97.4,
        "max_lat": 37.1,
    }

class RiskConstants:
    """Risk assessment constants."""
    CONFIDENCE_THRESHOLD = 0.7
    RAINFALL_WINDOW_HOURS = 72
    DEFAULT_MODEL_VERSION = "0.1.0"

class CacheConstants:
    """Redis cache constants."""
    RISK_ZONE_TTL = 3600  # 1 hour
    RESOURCE_TTL = 1800   # 30 minutes
    SHELTER_TTL = 1800    # 30 minutes
