from fastapi import APIRouter
from app.services.reservationService import simulate_reservation as handle_reservation
from app.schemas.reservation import ReservationResponse


router = APIRouter(
    prefix="/restaurants",
    tags=["Reservation"]
)

# This is a feature I have decided not to include because of api limitations
#opentable needs a screening process to be done, and yelp does not have
#reservations for a majority of their restaurants so I thought it didnt have much value to include,
# here is a simple mock call to how it would have been done. store the endpoint in a .ENV and pull it in
@router.post(
    "/{business_id}/reserve",
    summary="Simulate reservation request",
    description="Pretend to call an external API like OpenTable to reserve a table.",
    response_model=ReservationResponse,
)
def reserve_table(business_id: str):
    return handle_reservation(business_id)