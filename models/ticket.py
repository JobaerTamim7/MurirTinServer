from datetime import date
from pydantic import BaseModel
from typing import Optional

class TicketCreate(BaseModel):
    bus_id: int
    route_id: int
    travel_date: date
    price: float

class TicketResponse(TicketCreate):
    ticket_id: int
    user_id: str
    booking_time: str
