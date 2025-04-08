import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Optional, List

from app.models.recommendation import Recommendation
from app.models.business import Business
from app.schemas.recommendation import RecommendationCreate


def create_recommendation_entry(
    db: Session,
    recommendation: RecommendationCreate
) -> Recommendation:
    business = db.query(Business).filter(Business.id == recommendation.business_id).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    new_rec = Recommendation(
        id=str(uuid.uuid4()),
        business_id=recommendation.business_id,
        user_email=recommendation.user_email,
        suggest=recommendation.suggest,
        note=recommendation.note,
    )

    db.add(new_rec)
    db.commit()
    db.refresh(new_rec)
    return new_rec


def get_filtered_recommendations(
    db: Session,
    business_id: Optional[str],
    user_email: Optional[str]
) -> List[Recommendation]:
    query = db.query(Recommendation)

    if business_id:
        business_exists = db.query(Business.id).filter(Business.id == business_id).first()
        if not business_exists:
            raise HTTPException(status_code=404, detail="Business not found")
        query = query.filter(Recommendation.business_id == business_id)

    if user_email:
        query = query.filter(Recommendation.user_email == user_email)

    return query.all()
