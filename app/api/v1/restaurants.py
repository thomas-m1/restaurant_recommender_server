# Pydantic models

from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional, List
from app.schemas.restaurant import Restaurant, PaginatedRestaurants
from app.core.deps import get_resources
from app.core.config import settings
from app.utils.filters import (
    map_ambiance_to_term,
    map_cuisine_to_yelp_category,
    map_price_to_yelp,
    map_distance_to_radius_km,
    map_liked_by_to_yelp,
    format_liked_by_for_display
)
from app.utils.parsers import (
    format_hours,
    extract_tags_from_specialties,
    combine_display_tags
)

router = APIRouter()

# Office coordinates from environment
OFFICE_LAT = settings.OFFICE_LAT
OFFICE_LNG = settings.OFFICE_LNG


@router.get("/restaurants", response_model=PaginatedRestaurants)
async def get_restaurants(
    cuisine: Optional[str] = None,
    ambiance: Optional[str] = None,
    price: Optional[str] = None,
    distance: Optional[str] = None,
    rating: Optional[float] = Query(None, ge=0.0, le=5.0),
    liked_by: Optional[List[str]] = Query(None),
    sort_by: Optional[str] = Query("best_match"),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=50),
    resources = Depends(get_resources)
):
    # Construct search term
    term = "restaurant"
    if ambiance:
        ambiance_term = map_ambiance_to_term(ambiance)
        if ambiance_term:
            term += f" {ambiance_term}"

    # Map liked_by values
    selected_liked_by = [map_liked_by_to_yelp(tag) for tag in liked_by or []]
    selected_liked_by = list(filter(None, selected_liked_by))

    # Build Yelp query parameters
    params = {
        "term": term,
        "latitude": OFFICE_LAT,
        "longitude": OFFICE_LNG,
        "limit": per_page,
        "offset": (page - 1) * per_page,
        "sort_by": sort_by,
    }

    if cuisine:
        mapped_cuisine = map_cuisine_to_yelp_category(cuisine)
        if mapped_cuisine:
            params["categories"] = mapped_cuisine
    if price:
        mapped_price = map_price_to_yelp(price)
        if mapped_price:
            params["price"] = mapped_price
    if distance:
        params["radius"] = map_distance_to_radius_km(distance)

    try:
        yelp_data = await resources.yelp_client.search_restaurants(params)
        businesses = yelp_data.get("businesses", [])
        total = yelp_data.get("total", len(businesses))
    except Exception as e:
        raise HTTPException(status_code=502, detail="Failed to fetch data from Yelp")

    results = []

    for item in businesses:
        if rating and item.get("rating", 0) < rating:
            continue

        business_liked_by = item.get("liked_by", [])
        if selected_liked_by:
            if not set(business_liked_by).intersection(set(selected_liked_by)):
                continue

        display_liked_by = [
            format_liked_by_for_display(tag)
            for tag in business_liked_by
            if format_liked_by_for_display(tag)
        ]

        attributes = item.get("attributes", {})
        ambience_data = attributes.get("ambience", {})
        parking_data = attributes.get("business_parking", {})
        specialties = attributes.get("about_this_biz_specialties", "")

        formatted_hours = format_hours(item.get("business_hours", []))
        specialty_tags = extract_tags_from_specialties(specialties)
        display_tags = combine_display_tags(display_liked_by, ambience_data, specialty_tags)

        restaurant = Restaurant(
            id=item["id"],
            name=item["name"],
            rating=item["rating"],
            price=item.get("price"),
            location=", ".join(item["location"].get("display_address", [])),
            image_url=item.get("image_url", ""),
            photos=item.get("photos", []),
            phone=item.get("display_phone", ""),
            website=item.get("url"),
            yelp_url=item.get("url"),
            categories=[cat["title"] for cat in item.get("categories", [])],
            distance=item.get("distance"),

            # Enriched Fields
            hours=formatted_hours,
            tags=specialty_tags,
            reservation=attributes.get("restaurants_reservations", False),
            accepts_credit_cards=attributes.get("accepted_cards", {}).get("credit", False),
            ambience=", ".join([
                k.replace("_", " ").title() for k, v in ambience_data.items() if v
            ]) if ambience_data else None,
            liked_by=display_liked_by,
            noise_level=attributes.get("noise_level"),
            parking=", ".join([
                k.replace("_", " ").title() for k, v in parking_data.items() if v
            ]) if parking_data else None,
            outdoor_seating=attributes.get("outdoor_seating", False),
            display_tags=display_tags
        )
        print(restaurant)
        results.append(restaurant)

    return PaginatedRestaurants(
        total=total,
        page=page,
        per_page=per_page,
        results=results
    )




# from fastapi import APIRouter, Depends, Query, HTTPException
# from typing import Optional, List
# from app.schemas.restaurant import Restaurant, PaginatedRestaurants
# from app.core.deps import get_resources
# from app.core.config import settings
# from app.utils.filters import (
#     map_ambiance_to_term,
#     map_cuisine_to_yelp_category,
#     map_price_to_yelp,
#     map_distance_to_radius_km,
#     map_liked_by_to_yelp
# )

# router = APIRouter()

# # Office Coordinates
# OFFICE_LAT = settings.OFFICE_LAT
# OFFICE_LNG = settings.OFFICE_LNG

# @router.get("/restaurants", response_model=PaginatedRestaurants)
# async def get_restaurants(
#     cuisine: Optional[str] = None,
#     ambiance: Optional[str] = None,
#     price: Optional[str] = None,
#     distance: Optional[str] = None,
#     rating: Optional[float] = Query(None, ge=0.0, le=5.0),
#     liked_by: Optional[List[str]] = Query(None),
#     sort_by: Optional[str] = Query("best_match"),
#     page: int = Query(1, ge=1),
#     per_page: int = Query(10, ge=1, le=50),
#     resources = Depends(get_resources)
# ):
#     term = "restaurant"
#     if ambiance:
#         term += f" {map_ambiance_to_term(ambiance)}"

#     params = {
#         "term": term,
#         "latitude": OFFICE_LAT,
#         "longitude": OFFICE_LNG,
#         "limit": per_page,
#         "offset": (page - 1) * per_page,
#         "sort_by": sort_by
#     }

#     if cuisine:
#         params["categories"] = map_cuisine_to_yelp_category(cuisine)
#     if price:
#         params["price"] = map_price_to_yelp(price)
#     if distance:
#         params["radius"] = map_distance_to_radius_km(distance)

#     yelp_data = await resources.yelp_client.search_restaurants(params)
#     print(yelp_data.get("businesses", []))

#     results = []
#     for item in yelp_data.get("businesses", []):
#         if rating and item.get("rating", 0) < rating:
#             continue

#         restaurant = Restaurant(
#             id=item["id"],
#             name=item["name"],
#             rating=item["rating"],
#             price=item.get("price"),
#             location=", ".join(item["location"].get("display_address", [])),
#             image_url=item.get("image_url", ""),
#             photos=item.get("photos", []),
#             phone=item.get("display_phone", ""),
#             website=item.get("url"),
#             categories=[cat["title"] for cat in item.get("categories", [])],
#             distance=item.get("distance"),
#             # Enriched fields (to implement or simulate)
#             tags=[],
#             hours=[],
#             reservation=False,
#             accepts_credit_cards=False,
#             ambience=ambiance or None,
#             liked_by=[],
#             noise_level=None,
#             parking=None,
#             outdoor_seating=False
#         )
#         results.append(restaurant)

#     return PaginatedRestaurants(
#         total=yelp_data.get("total", len(results)),
#         page=page,
#         per_page=per_page,
#         results=results
#     )
