from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.schemas.restaurant import RestaurantOut
from app.schemas.pagination import PaginatedResponse  # ✅ import this
from app.core.deps import get_db
from app.services.restaurant_service import fetch_filtered_restaurants

router = APIRouter(
    prefix="/restaurants",
    tags=["Restaurants"]
)

@router.get(
    "/",
    response_model=PaginatedResponse[RestaurantOut],
    summary="Get filtered restaurants",
    description="Fetch restaurants using filters like cuisine, price, occasion tags, distance from office, and other partner-specific preferences.",
    responses={
        200: {"description": "Restaurants successfully retrieved"},
        400: {"description": "Invalid query parameters"},
    }
)
def get_restaurants(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 12,
    scenario_tag: Optional[str] = Query(None),
    categories: Optional[List[str]] = Query(None),
    price: Optional[List[str]] = Query(None),
    sort_by: str = Query("best_match", enum=["best_match", "highest_rated", "popularity", "distance"]),
    outdoor_seating: Optional[bool] = Query(None),
    good_for_groups: Optional[bool] = Query(None),
    max_distance_km: Optional[float] = Query(None),
    good_for_meal: Optional[List[str]] = Query(None),
):
    return fetch_filtered_restaurants(
        db=db,
        skip=skip,
        limit=limit,
        scenario_tag=scenario_tag,
        categories=categories,
        price=price,
        sort_by=sort_by,
        outdoor_seating=outdoor_seating,
        good_for_groups=good_for_groups,
        max_distance_km=max_distance_km,
        good_for_meal=good_for_meal,
    )
