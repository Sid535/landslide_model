"""Main FastAPI application."""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import settings
from .database import check_database_connection, close_database
from .exceptions import LandslideError
from .routers.v1 import router as v1_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting Landslide Risk Assessment API")
    logger.info(f"Environment: {settings.environment}")
    
    # Check database connection
    db_status = await check_database_connection()
    if db_status["status"] == "healthy":
        logger.info("✅ Database connection successful")
    else:
        logger.warning(f"⚠️ Database connection failed: {db_status.get('error')}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Landslide Risk Assessment API")
    await close_database()


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="Backend for landslide risk prediction and resource allocation",
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Error handlers
@app.exception_handler(LandslideError)
async def landslide_error_handler(request: Request, exc: LandslideError):
    """Handle custom application errors."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.error_code,
                "message": exc.message,
                "details": exc.details,
            }
        },
    )


@app.exception_handler(Exception)
async def general_error_handler(request: Request, exc: Exception):
    """Handle unexpected errors."""
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred",
            }
        },
    )


# Health check endpoints
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Landslide Risk Assessment API",
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
async def health():
    """Basic health check."""
    return {"status": "healthy"}


@app.get("/health/detailed")
async def detailed_health():
    """Detailed health check with dependencies."""
    db_status = await check_database_connection()
    
    all_healthy = db_status["status"] == "healthy"
    
    return {
        "status": "healthy" if all_healthy else "degraded",
        "checks": {
            "database": db_status,
        },
        "timestamp": "2024-01-01T00:00:00Z",  # Use datetime.utcnow() in production
    }


# Include API routes
app.include_router(
    v1_router,
    prefix=settings.api_v1_prefix,
)
