from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
from sqlalchemy import case, func

from app.models.business import Business
from app.schemas.restaurant import RestaurantOut
from sqlalchemy.orm import selectinload
from sqlalchemy import or_

from app.core.deps import get_db
from app.utils.filters import case_insensitive_json_array_filter


router = APIRouter(prefix="/restaurants", tags=["Restaurants"])


@router.get("/", response_model=List[RestaurantOut])
def get_restaurants(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 15,
    scenario_tag: Optional[str] = Query(None),
    categories: Optional[List[str]] = Query(None),
    price: Optional[List[str]] = Query(None),
    sort_by: str = Query("best_match", enum=["best_match", "highest_rated", "popularity", "distance"]),
    outdoor_seating: Optional[bool] = Query(None),
    good_for_groups: Optional[bool] = Query(None),
    max_distance_km: Optional[float] = Query(None),
    good_for_meal: Optional[List[str]] = Query(None),
):
    query = db.query(Business).options(selectinload(Business.recommendations))
    query = db.query(Business).filter(Business.is_closed == False)

    if categories:
        category_clauses = [
            text(case_insensitive_json_array_filter("categories", category))
            for category in categories
        ]
        query = query.filter(or_(*category_clauses))

    if scenario_tag:
        sql_clause = case_insensitive_json_array_filter("scenario_tags", scenario_tag)
        query = query.filter(text(sql_clause))

    if price:
        query = query.filter(Business.price.in_(price))

    if outdoor_seating is not None:
        query = query.filter(Business.outdoor_seating == outdoor_seating)

    if good_for_groups is not None:
        query = query.filter(Business.good_for_groups == good_for_groups)

    if max_distance_km is not None:
        query = query.filter(Business.distance_from_office_km <= max_distance_km)

    if good_for_meal:
        meal_clauses = [
            text(f"(good_for_meal ->> '{tag}')::boolean = true") for tag in good_for_meal
        ]
        query = query.filter(or_(*meal_clauses))


    # sorting
    if sort_by == "best_match":
        match_score = (Business.rating * 0.8) + (func.ln(Business.review_count + 1) * 0.2)
        query = query.order_by(match_score.desc())
    elif sort_by == "highest_rated":
        query = query.order_by(Business.rating.desc(), Business.review_count.desc())
    elif sort_by == "popularity":
        query = query.order_by(Business.review_count.desc())
    elif sort_by == "distance":
        query = query.order_by(Business.distance_from_office_km.asc())

    restaurants = query.offset(skip).limit(limit).all()


    return restaurants
