
from pydantic import BaseModel
from typing import List, Optional, Dict
from app.schemas.recommendation import RecommendationOut


class RestaurantOut(BaseModel):
    id: str
    name: str
    categories: List[str]
    price: Optional[str]
    rating: float
    review_count: int
    address: str
    latitude: float
    longitude: float
    distance_from_office_km: float
    phone: Optional[str]
    image_url: Optional[str]
    url: Optional[str]
    is_closed: bool
    scenario_tags: List[str]

    # Premium / enriched fields
    website: Optional[str]
    accepts_credit_cards: Optional[bool]
    alcohol: Optional[str]
    ambience: Optional[Dict[str, Optional[bool]]]
    good_for_meal: Optional[Dict[str, Optional[bool]]]
    noise_level: Optional[str]
    attire: Optional[str]
    good_for_groups: Optional[bool]
    outdoor_seating: Optional[bool]
    business_hours: Optional[List[Dict]]
    recommendations: Optional[List[RecommendationOut]]


    class Config:
        orm_mode = True


