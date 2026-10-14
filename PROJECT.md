# Landslide Risk Assessment Platform - Project Documentation

## Project Overview
A comprehensive landslide risk assessment platform with two main tracks:
- **Track A**: Machine Learning pipeline for landslide prediction
- **Track B**: Backend platform for risk assessment and resource allocation

## Current Status
- ✅ Backend structure complete
- ✅ 51 tests passing (no warnings)
- ✅ Docker services running (PostgreSQL, Redis, RabbitMQ)
- ✅ API endpoints functional
- ✅ Data models with PostGIS geospatial support

---

## Project Structure
landslide_model/
├── pyproject.toml # Root workspace config
├── uv.lock # Shared lockfile
├── data/ # ML training data (Track A)
├── models/ # ML model checkpoints (Track A)
├── notebooks/ # Jupyter notebooks (Track A)
├── src/landslide_model/ # Track A: ML pipeline
└── backend/ # Track B: FastAPI backend
├── pyproject.toml # Backend package config
├── docker-compose.yml # Infrastructure services
├── pytest.ini # Pytest configuration
├── .env # Local environment variables
├── .gitignore # Git ignore rules
├── README.md # Backend README
├── src/landslide_backend/
│ ├── init.py
│ ├── main.py # FastAPI app entry point
│ ├── config.py # Settings management
│ ├── database.py # Database connection
│ ├── constants.py # Application constants
│ ├── exceptions.py # Custom exceptions
│ ├── init_db.py # Database initialization
│ ├── models/
│ │ ├── init.py
│ │ ├── enums.py # All enums (centralized)
│ │ ├── db.py # SQLAlchemy models
│ │ └── schemas.py # Pydantic schemas
│ ├── repositories/ # Data access layer
│ │ ├── init.py
│ │ ├── base_repo.py # Base repository (CRUD)
│ │ ├── risk_zone_repo.py # Risk zone queries
│ │ ├── resource_repo.py # Resource queries
│ │ └── shelter_repo.py # Shelter queries
│ ├── services/ # Business logic layer
│ │ ├── init.py
│ │ ├── risk_service.py # Risk assessment logic
│ │ ├── resource_service.py # Resource management
│ │ └── shelter_service.py # Shelter management
│ ├── routers/ # API endpoints
│ │ ├── init.py
│ │ └── v1/
│ │ ├── init.py # V1 router aggregation
│ │ ├── risk.py # Risk zone endpoints
│ │ ├── resources.py # Resource endpoints
│ │ └── shelters.py # Shelter endpoints
│ └── tasks/ # Background tasks (empty)
│ └── init.py
└── tests/ # Test suite
├── init.py
├── conftest.py # Test fixtures
├── test_enums.py # Enum tests
├── test_schemas.py # Schema validation tests
├── test_models.py # Database model tests
└── test_api.py # API integration tests


---

## Architecture

### Layered Architecture

HTTP Request → Router (API Layer) → Service (Business Logic) → Repository (Data Access) → Database


### Key Components

#### 1. Configuration (`config.py`)
- Environment-based settings using pydantic-settings
- Database URL, Redis URL, RabbitMQ URL
- CORS origins
- Model checkpoint path

#### 2. Database (`database.py`)
- Async SQLAlchemy engine
- PostgreSQL with PostGIS extension
- Session management with dependency injection
- Connection health checks

#### 3. Models (`models/`)
- **Enums**: Type-safe enumerations for all domain concepts
- **DB Models**: SQLAlchemy ORM models with PostGIS geometry
- **Schemas**: Pydantic models for API validation

#### 4. Repositories (`repositories/`)
- Generic CRUD operations
- Entity-specific queries
- Data access abstraction

#### 5. Services (`services/`)
- Business logic implementation
- Geometry conversion (lat/lon ↔ WKT)
- Validation rules
- Error handling

#### 6. Routers (`routers/`)
- RESTful API endpoints
- Versioned at `/api/v1/`
- Request/response validation
- HTTP status codes

---

## Database Schema

### risk_zones
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| grid_cell_id | String | Unique grid cell identifier |
| risk_tier | Enum | watch/alert/evacuate |
| confidence | Float | 0-1 confidence score |
| geometry | Geometry(Polygon) | Geographic boundary |
| rainfall_data | JSON | Recent rainfall data |
| model_version | String | ML model version |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

### resources
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| name | String | Resource name |
| resource_type | Enum | medical/rescue/shelter/food/water/transport/communication |
| capacity | Integer | Total capacity |
| location | Geometry(Point) | Geographic location |
| status | Enum | available/deployed/maintenance/depleted |
| contact_info | JSON | Contact details |
| created_at | DateTime | Creation timestamp |

### shelters
| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| name | String | Shelter name |
| capacity | Integer | Maximum capacity |
| current_occupancy | Integer | Current occupancy |
| location | Geometry(Point) | Geographic location |
| facilities | JSON | Available facilities |
| status | Enum | open/full/closed |
| created_at | DateTime | Creation timestamp |

---

## API Endpoints

### Health Checks
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint |
| GET | `/health` | Basic health check |
| GET | `/health/detailed` | Detailed health with dependencies |

### Risk Zones (`/api/v1/risk-zones`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/` | Create risk zone |
| GET | `/` | List all risk zones |
| GET | `/high-risk` | Get high-risk zones |
| GET | `/tier/{tier}` | Get zones by tier |
| GET | `/{zone_id}` | Get zone by ID |
| PUT | `/{zone_id}` | Update zone |
| DELETE | `/{zone_id}` | Delete zone |

### Resources (`/api/v1/resources`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/` | Create resource |
| GET | `/` | List all resources |
| GET | `/available` | Get available resources |
| GET | `/type/{type}` | Get resources by type |
| GET | `/{resource_id}` | Get resource by ID |
| PUT | `/{resource_id}` | Update resource |
| DELETE | `/{resource_id}` | Delete resource |

### Shelters (`/api/v1/shelters`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/` | Create shelter |
| GET | `/` | List all shelters |
| GET | `/open` | Get open shelters |
| GET | `/with-capacity` | Get shelters with capacity |
| GET | `/{shelter_id}` | Get shelter by ID |
| PUT | `/{shelter_id}` | Update shelter |
| DELETE | `/{shelter_id}` | Delete shelter |

---

## Infrastructure

### Docker Services
| Service | Image | Port | Purpose |
|---------|-------|------|---------|
| PostgreSQL | postgis/postgis:16-3.4 | 5432 | Database with geospatial support |
| Redis | redis:7-alpine | 6379 | Caching |
| RabbitMQ | rabbitmq:3-management | 5672, 15672 | Message queue |

### Environment Variables (`.env`)
```env
DATABASE_URL=postgresql+asyncpg://landslide:landslide@localhost:5432/landslide_db
REDIS_URL=redis://localhost:6379/0
RABBITMQ_URL=amqp://guest:guest@localhost:5672/
OSRM_URL=http://localhost:5000
MODEL_CHECKPOINT_PATH=../../models/best_model.pt

Testing
Test Statistics

    Total tests: 51

    Pass rate: 100%

    Warnings: 0

    Execution time: ~2.4 seconds

Test Categories
Category	Tests	Description
Enums	11	Test enum values and properties
Schemas	22	Test Pydantic validation
Models	12	Test database model definitions
API	6	Test API endpoints
Running Tests

# Run all tests
uv run pytest backend/tests/ -v

# Run specific test file
uv run pytest backend/tests/test_schemas.py -v

# Run with coverage
uv run pytest backend/tests/ --cov=landslide_backend --cov-report=html

Design Patterns & Best Practices
1. Repository Pattern

Separates data access logic from business logic.
2. Service Layer

Contains business rules and validation.
3. Dependency Injection

FastAPI's Depends for database sessions.
4. Custom Exceptions

Typed error handling with status codes.
5. Enums

Type-safe constants for domain concepts.
6. Pydantic Settings

Environment-based configuration.
7. Async/Await

Full async database operations.
8. API Versioning

Versioned endpoints for future compatibility.
9. Geometry Handling

WKT format for PostGIS, lat/lon for API.
Key Decisions

    PostgreSQL + PostGIS: Chosen for geospatial queries

    SQLAlchemy Async: Full async database operations

    Repository Pattern: Clean separation of concerns

    Pydantic v2: Modern validation with model_validator

    pytest: Async test support, simpler syntax

    uv Workspace: Monorepo management for both tracks

    Session-scoped event loop: Avoids asyncpg loop issues

Next Steps (Track B)
Step 2: Data Ingestion

    IMD rainfall data integration

    Scheduled data fetching

    Historical data replay

Step 3: Caching & Queue

    Redis for risk tier caching

    RabbitMQ for async tasks

    Cache invalidation strategy

Step 4: Resource Allocation

    Priority-based allocation

    Linear programming optimization

    Real-time updates

Step 5: Evacuation Routing

    OSRM integration

    Route calculation

    Shelter assignment

Step 6: Frontend

    React dashboard

    Map visualization

    Real-time updates

Step 7: Auth & Notifications

    Authentication

    Push notifications

    Alert system

Step 8: DevOps

    Docker containers

    CI/CD pipeline

    Monitoring

Step 9: Integration

    Connect ML model

    End-to-end testing

    Production deployment

Commands Reference
bash

# Start infrastructure
cd backend && docker compose up -d

# Initialize database
cd backend/src/landslide_backend && uv run python init_db.py

# Start API server
uv run --package landslide-backend uvicorn landslide_backend.main:app --reload

# Run tests
uv run pytest backend/tests/ -v

# Sync dependencies
uv sync --all-packages --extra dev

# View API documentation
# http://localhost:8000/docs
# http://localhost:8000/redoc
---

## Addendum: Design Decisions Log

### Decision 1: Shelter is not a ResourceType
**Date**: Documented during Phase 0 review.

**Context**: The original `ResourceType` enum included `SHELTER` as one of seven values, while `Shelter` also existed as a first-class table with its own capacity, occupancy, and status.

**Decision**: Removed `SHELTER` from `ResourceType`. Shelters are now the sole source of truth for shelter data.

**Rationale**: 
- Shelters are destination points for evacuation routing, not dispatchable resources.
- Shelters don't get "sent" anywhere — they have capacity/occupancy that changes over time.
- Having two tables represent the same concept created ambiguity in resource allocation queries.
- The allocation optimizer will now only query `resources` for dispatchable assets and `shelters` for evacuation destinations.
