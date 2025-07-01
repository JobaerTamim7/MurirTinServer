# routers/ticket.py
from fastapi import APIRouter, Depends, status
from models.ticket import BookTicketRequest, TicketBookingResponse
from services import ticket_service
from utils.jwt_token import get_current_user

router = APIRouter(
    prefix="/ticket",
    tags=["Ticket Booking"],
)

@router.post("/book", response_model=TicketBookingResponse, status_code=status.HTTP_201_CREATED)
async def book_ticket_route(
    request: BookTicketRequest, 
    current_user: dict = Depends(get_current_user) 
):
    return await ticket_service.book_tickets(request, current_user)