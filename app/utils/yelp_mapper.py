from app.schemas.restaurant import Restaurant
from app.utils.filters import format_liked_by_for_display
from typing import List

def map_yelp_business_to_restaurant(item: dict, requested_ambience: str = None) -> Restaurant:
    liked_by_raw = item.get("liked_by", [])
    display_liked_by = [
        format_liked_by_for_display(tag) for tag in liked_by_raw
        if format_liked_by_for_display(tag)
    ]

    return Restaurant(
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
        tags=[],  # future enrichment
        hours=[],  # Requires Business Details endpoint
        reservation=False,
        accepts_credit_cards=False,
        ambience=requested_ambience,
        liked_by=display_liked_by,
        noise_level=None,
        parking=None,
        outdoor_seating=False
    )
