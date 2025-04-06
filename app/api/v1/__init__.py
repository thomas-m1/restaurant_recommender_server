from fastapi import APIRouter
from . import restaurants, system

router = APIRouter()

router.include_router(system.router, tags=["System"])
router.include_router(restaurants.router, tags=["Restaurants"])
