from pydantic import BaseModel, EmailStr
from typing import Optional

class RecommendationCreate(BaseModel):
    business_id: str
    user_email: EmailStr
    suggest: bool
    note: Optional[str] = None

class RecommendationOut(RecommendationCreate):
    id: str

    class Config:
        orm_mode = True
