from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.deps import get_db
from app.schemas.recommendation import RecommendationCreate, RecommendationOut
from app.services.recommendation_service import (
    create_recommendation_entry,
    get_filtered_recommendations,
)

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"]
)

#this functionality can get extended.
# ie each user will have a list of likes/comments they made and and can
# update their suggestions using a put operation
@router.post(
    "/",
    response_model=RecommendationOut,
    summary="Submit a recommendation",
    description="Create a new partner recommendation (like or dislike) for a specific restaurant, with an optional comment.",
    responses={
        201: {"description": "Recommendation created successfully"},
        404: {"description": "Business not found"},
    }
)
def create_recommendation(
    recommendation: RecommendationCreate,
    db: Session = Depends(get_db)
):
    return create_recommendation_entry(db, recommendation)



#optional to get restaurants recommended by a user - could implement with auth
# can also extend to get all of a users likes and comments
@router.get(
    "/",
    response_model=List[RecommendationOut],
    summary="Get recommendations",
    description="Retrieve all partner recommendations by either `business_id` or `user_email`.",
    responses={
        200: {"description": "Successfully retrieved recommendations"},
        400: {"description": "Must provide either business_id or user_email"},
        404: {"description": "Business not found"},
    }
)
def get_recommendations(
    business_id: Optional[str] = Query(None),
    user_email: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    if not business_id and not user_email:
        raise HTTPException(
            status_code=400,
            detail="You must provide either business_id or user_email"
        )
    return get_filtered_recommendations(db, business_id, user_email)
