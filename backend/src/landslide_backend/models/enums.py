"""Centralized enums for the landslide backend."""
import enum
from typing import List


class RiskTier(str, enum.Enum):
    """Risk levels for landslide prediction."""
    WATCH = "watch"
    ALERT = "alert"
    EVACUATE = "evacuate"
    
    @property
    def severity_level(self) -> int:
        """Numeric severity for sorting and comparison."""
        return {
            RiskTier.WATCH: 1,
            RiskTier.ALERT: 2,
            RiskTier.EVACUATE: 3,
        }[self]
    
    @property
    def color(self) -> str:
        """Color for map visualization."""
        return {
            RiskTier.WATCH: "#FFD700",    # Gold
            RiskTier.ALERT: "#FF8C00",    # Orange
            RiskTier.EVACUATE: "#FF0000", # Red
        }[self]


class ResourceType(str, enum.Enum):
    """Types of dispatchable emergency resources.
    
    Note: Shelter is intentionally NOT included here.
    Shelters are destination points for evacuation routing,
    not dispatchable resources that get deployed to incident sites.
    They are managed separately in the Shelter model.
    """
    MEDICAL = "medical"
    RESCUE = "rescue"
    FOOD = "food"
    WATER = "water"
    TRANSPORT = "transport"
    COMMUNICATION = "communication"


class ResourceStatus(str, enum.Enum):
    """Status of resources."""
    AVAILABLE = "available"
    DEPLOYED = "deployed"
    MAINTENANCE = "maintenance"
    DEPLETED = "depleted"


class ShelterStatus(str, enum.Enum):
    """Status of shelters."""
    OPEN = "open"
    FULL = "full"
    CLOSED = "closed"


class FacilityType(str, enum.Enum):
    """Facilities available at shelters."""
    MEDICAL = "medical"
    FOOD = "food"
    WATER = "water"
    SANITATION = "sanitation"
    POWER = "power"
    COMMUNICATION = "communication"
    ACCESSIBILITY = "accessibility"


class APIStatus(str, enum.Enum):
    """Standard API response statuses."""
    SUCCESS = "success"
    ERROR = "error"
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskStatus(str, enum.Enum):
    """Status for background tasks."""
    QUEUED = "queued"
    RUNNING = "running"
    RETRYING = "retrying"
    SUCCESS = "success"
    FAILURE = "failure"


class TaskType(str, enum.Enum):
    """Types of background tasks."""
    DATA_INGESTION = "data_ingestion"
    RISK_COMPUTATION = "risk_computation"
    RESOURCE_ALLOCATION = "resource_allocation"
    ROUTE_CALCULATION = "route_calculation"
    NOTIFICATION = "notification"


class NotificationType(str, enum.Enum):
    """Types of notifications."""
    WATCH_ALERT = "watch_alert"
    ALERT_ESCALATION = "alert_escalation"
    EVACUATION_ORDER = "evacuation_order"
    RESOURCE_DEPLOYED = "resource_deployed"
    SHELTER_OPENED = "shelter_opened"
    SYSTEM_ERROR = "system_error"


class NotificationPriority(enum.IntEnum):
    """Priority levels for notifications."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4
    EMERGENCY = 5


class ModelType(str, enum.Enum):
    """Types of ML models."""
    CNN = "cnn"
    LSTM = "lstm"
    HYBRID = "hybrid"
    ENSEMBLE = "ensemble"


class ModelStatus(str, enum.Enum):
    """Status of ML models."""
    TRAINING = "training"
    VALIDATING = "validating"
    PRODUCTION = "production"
    RETIRED = "retired"
    FAILED = "failed"


class DataSource(str, enum.Enum):
    """Sources of data."""
    SATELLITE = "satellite"
    RAINFALL = "rainfall"
    TERRAIN = "terrain"
    HISTORICAL = "historical"
    REAL_TIME = "real_time"


class RouteStatus(str, enum.Enum):
    """Status of evacuation routes."""
    CALCULATING = "calculating"
    AVAILABLE = "available"
    BLOCKED = "blocked"
    CONGESTED = "congested"
    CLOSED = "closed"


class TransportationMode(str, enum.Enum):
    """Modes of transportation for evacuation."""
    WALKING = "walking"
    DRIVING = "driving"
    BICYCLING = "bicycling"
    TRANSIT = "transit"


class ErrorCode(str, enum.Enum):
    """Standard error codes."""
    INVALID_INPUT = "INVALID_INPUT"
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    DATABASE_ERROR = "DATABASE_ERROR"
    MODEL_ERROR = "MODEL_ERROR"
    ROUTING_ERROR = "ROUTING_ERROR"
    AUTH_ERROR = "AUTH_ERROR"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    EXTERNAL_SERVICE_ERROR = "EXTERNAL_SERVICE_ERROR"
