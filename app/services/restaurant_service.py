from sqlalchemy.orm import Session, selectinload
from sqlalchemy import func, text, or_

from app.models.business import Business
from app.utils.filters import case_insensitive_json_array_filter
from app.schemas.restaurant import RestaurantOut
from app.schemas.pagination import PaginatedResponse

def fetch_filtered_restaurants(
    db: Session,
    skip: int,
    limit: int,
    scenario_tag: str | None,
    categories: list[str] | None,
    price: list[str] | None,
    sort_by: str,
    outdoor_seating: bool | None,
    good_for_groups: bool | None,
    max_distance_km: float | None,
    good_for_meal: list[str] | None,
) -> PaginatedResponse[RestaurantOut]:
    query = db.query(Business).options(selectinload(Business.recommendations))
    query = query.filter(Business.is_closed == False)

    # make sure filters case
    if categories:
        category_clauses = [
            text(case_insensitive_json_array_filter("categories", category))
            for category in categories
        ]
        query = query.filter(or_(*category_clauses))

    if scenario_tag:
        sql_clause = case_insensitive_json_array_filter("scenario_tags", scenario_tag)
        query = query.filter(text(sql_clause))

    if good_for_meal:
        meal_clauses = [
            text(f"(good_for_meal ->> '{tag}')::boolean = true") for tag in good_for_meal
        ]
        query = query.filter(or_(*meal_clauses))

    if price:
        query = query.filter(Business.price.in_(price))

    if outdoor_seating is not None:
        query = query.filter(Business.outdoor_seating == outdoor_seating)

    if good_for_groups is not None:
        query = query.filter(Business.good_for_groups == good_for_groups)

    if max_distance_km is not None:
        query = query.filter(Business.distance_from_office_km <= max_distance_km)

    # Total count before pagination
    total = query.count()

    # Sorting
    if sort_by == "best_match":
        match_score = (Business.rating * 0.8) + (func.ln(Business.review_count + 1) * 0.2)
        query = query.order_by(match_score.desc())
    elif sort_by == "highest_rated":
        query = query.order_by(Business.rating.desc(), Business.review_count.desc())
    elif sort_by == "popularity":
        query = query.order_by(Business.review_count.desc())
    elif sort_by == "distance":
        query = query.order_by(Business.distance_from_office_km.asc())

    items = query.offset(skip).limit(limit).all()

    return PaginatedResponse(
        total=total,
        limit=limit,
        offset=skip,
        items=items,
    )