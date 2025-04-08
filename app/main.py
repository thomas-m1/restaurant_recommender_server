from fastapi import FastAPI
from app.api.v1 import router as api_router
from app.core import init_app
from app.core.config import get_settings
from app.core.error_handler import (
    http_exception_handler,
    validation_exception_handler,
    unhandled_exception_handler
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

# Tags for OpenAPI docs
tags_metadata = [
    {
        "name": "Restaurants",
        "description": "Endpoints to browse and filter restaurants based on categories, tags, distance, and more.",
    },
    {
        "name": "Recommendations",
        "description": "Endpoints to submit and retrieve partner recommendations for restaurants.",
    },
]

# Load settings
settings = get_settings()

app = FastAPI(
    title="Bain Restaurant Recommender",
    version=settings.APP_VERSION,
    description="MVP for Bain Partners to find client-appropriate restaurants",
    openapi_tags=tags_metadata,
    docs_url="/docs" if settings.ENV == "development" else None,
    redoc_url=None,
    openapi_url="/openapi.json" if settings.ENV == "development" else None,
)

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

init_app(app)

# Mount v1 API under versioned prefix
app.include_router(api_router, prefix="/api/v1")
