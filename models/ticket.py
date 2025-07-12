from pydantic import BaseModel
from typing import Optional

class BookTicketRequest(BaseModel):
    route_id: int
    from_location: str
    from_location_long: float
    from_location_lat: float
    to_location:str
    to_location_long: float
    to_location_lat: float
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




