from fastapi import APIRouter, Depends, status, HTTPException
from models.qr_code import TicketData
from services.qr_service import get_ticket_data
from utils.jwt_token import get_current_user # Ensure this utility exists and works correctly

router = APIRouter()

@router.get("/qr-data/{ticket_id}",
    response_model=TicketData,
    tags=["QR Code Data"],
    summary="Get Ticket Data for QR Code Generation",
    responses={
        200: {"description": "Successful response with ticket data."},
        401: {"description": "Unauthorized - Missing or invalid token."},
        403: {"description": "Forbidden - User does not own the ticket or lacks permission."},
        404: {"description": "Not Found - Ticket with the given ID does not exist."},
        500: {"description": "Internal Server Error - An unexpected error occurred on the server."}
    }
)
async def get_qr_data_endpoint(
    ticket_id: int, 
    current_user: dict = Depends(get_current_user) # Dependency to get the authenticated user
):
    """
    Provides the necessary data for a specific ticket ID.

    This endpoint is called by the Flutter app to get the information
    it needs to generate the QR code locally. A valid JWT token is required.

    - **ticket_id**: The unique identifier for the ticket booking.
    """
    # Pass the current_user to the service layer for authorization
    return await get_ticket_data(ticket_id, current_user)