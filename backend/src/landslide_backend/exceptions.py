"""Custom exceptions for the landslide backend."""
from typing import Optional
from .models.enums import ErrorCode


class LandslideError(Exception):
    """Base exception for application errors."""
    
    def __init__(
        self,
        message: str,
        error_code: ErrorCode,
        status_code: int = 400,
        details: Optional[dict] = None,
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)


class ResourceNotFoundError(LandslideError):
    """Raised when a requested resource doesn't exist."""
    
    def __init__(self, resource_type: str, resource_id: str):
        super().__init__(
            message=f"{resource_type} with id '{resource_id}' not found",
            error_code=ErrorCode.RESOURCE_NOT_FOUND,
            status_code=404,
        )


class ValidationError(LandslideError):
    """Raised when input validation fails."""
    
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(
            message=message,
            error_code=ErrorCode.INVALID_INPUT,
            status_code=422,
            details=details,
        )


class DatabaseError(LandslideError):
    """Raised when database operations fail."""
    
    def __init__(self, message: str = "Database operation failed"):
        super().__init__(
            message=message,
            error_code=ErrorCode.DATABASE_ERROR,
            status_code=500,
        )


class ModelError(LandslideError):
    """Raised when ML model operations fail."""
    
    def __init__(self, message: str = "Model operation failed"):
        super().__init__(
            message=message,
            error_code=ErrorCode.MODEL_ERROR,
            status_code=500,
        )


class ExternalServiceError(LandslideError):
    """Raised when external services (OSRM, IMD) fail."""
    
    def __init__(self, service: str, message: str = "External service error"):
        super().__init__(
            message=f"{service}: {message}",
            error_code=ErrorCode.EXTERNAL_SERVICE_ERROR,
            status_code=503,
        )
