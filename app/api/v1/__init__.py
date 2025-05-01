from fastapi import APIRouter
from . import restaurants, system, recommendations, reservation

router = APIRouter()

router.include_router(system.router, tags=["System"])
router.include_router(restaurants.router, tags=["Restaurants"])
router.include_router(recommendations.router, tags=["Recommendations"])
router.include_router(reservation.router, tags=["Reservation"])
