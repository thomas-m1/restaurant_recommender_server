from fastapi import APIRouter, Depends
from app.core.deps import get_resources
from app.core.config import settings

router = APIRouter()

@router.get("/ping")
async def ping():
    return {"status": "ok", "message": "Server is alive."}

@router.get("/health")
async def health_check(resources = Depends(get_resources)):
    try:
        if resources.yelp_client:
            return {"status": "ok", "yelp_client": "initialized"}
    except Exception:
        return {"status": "error", "yelp_client": "unavailable"}

    return {"status": "unknown"}


@router.get("/version")
async def version():
    return {
        "version": settings.APP_VERSION,
        "environment": settings.ENV
    }