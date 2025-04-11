def simulate_reservation(business_id: str) -> dict:
    # Simulated logic for a reservation (could later call an external API - would use smthn like  OpenTable)
    return {
        "message": f"Reservation request for business {business_id}. This is a mock call - - no action taken",
        "status": "success",
    }
