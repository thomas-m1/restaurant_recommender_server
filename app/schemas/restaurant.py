from pydantic import BaseModel
from typing import List, Optional

class Restaurant(BaseModel):
    id: str
    name: str
    rating: float
    price: Optional[str]
    location: str
    image_url: Optional[str]
    photos: Optional[List[str]] = []
    categories: List[str]
    distance: Optional[float]
    phone: Optional[str]
    website: Optional[str]
    yelp_url: Optional[str]
    tags: List[str] = []
    hours: Optional[List[str]] = []
    reservation: Optional[bool] = False
    accepts_credit_cards: Optional[bool] = False
    ambience: Optional[str]
    liked_by: Optional[List[str]] = []
    noise_level: Optional[str]
    parking: Optional[str]
    outdoor_seating: Optional[bool]
    display_tags: List[str] = []


    class Config:
        orm_mode = True

class PaginatedRestaurants(BaseModel):
    total: int
    page: int
    per_page: int
    results: List[Restaurant]
