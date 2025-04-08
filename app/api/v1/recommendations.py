import uuid
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.deps import get_db
from app.models.recommendation import Recommendation
from app.models.business import Business
from app.schemas.recommendation import RecommendationCreate, RecommendationOut

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

#post endpoint to create a recommendation
@router.post("/", response_model=RecommendationOut)
def create_recommendation(
    recommendation: RecommendationCreate,
    db: Session = Depends(get_db)
):
    business = db.query(Business).filter(Business.id == recommendation.business_id).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    new_rec = Recommendation(
        id=str(uuid.uuid4()),
        business_id=recommendation.business_id,
        user_email=recommendation.user_email,
        suggest=recommendation.suggest,
        note=recommendation.note
    )
    db.add(new_rec)
    db.commit()
    db.refresh(new_rec)
    return new_rec


#for future if you want to filter by user_email or business_id
@router.get("/", response_model=List[RecommendationOut])
def get_recommendations(
    business_id: Optional[str] = Query(None),
    user_email: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    # Must provide at least one query parameter
    if not business_id and not user_email:
        raise HTTPException(
            status_code=400, detail="You must provide either business_id or user_email"
        )

    query = db.query(Recommendation)

    # Optional filtering by business_id
    if business_id:
        business_exists = db.query(Business.id).filter(Business.id == business_id).first()
        if not business_exists:
            raise HTTPException(status_code=404, detail="Business not found")
        query = query.filter(Recommendation.business_id == business_id)

    # Optional filtering by user_email
    if user_email:
        query = query.filter(Recommendation.user_email == user_email)

    return query.all()
