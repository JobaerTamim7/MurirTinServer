from pydantic import BaseModel
from typing import Optional

class BookTicketRequest(BaseModel):
    from_location: str
    to_location: str
    ticket_count: int

class TicketBookingResponse(BaseModel):
    message: str
    ticket_count: int
    total_cost: int
    booking_id: str

class BusRoute(BaseModel):
    id: int
    from_location: str
    to_location: str
    price: int
    available_seats: int




