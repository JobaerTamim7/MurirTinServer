#models/qr_code.py
from pydantic import BaseModel
import uuid

class TicketData(BaseModel):
    """
    Pydantic model to represent the data to be encoded in the QR code.
    """
    id: int
    user_id: uuid.UUID
    route_id: int
    from_location: str
    to_location: str
    ticket_count: int
    total_cost: int


