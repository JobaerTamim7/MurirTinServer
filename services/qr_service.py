from fastapi import HTTPException, status
import uuid  
from database import supabase
from models.qr_code import TicketData

async def get_ticket_data(ticket_id: int, current_user: dict) -> TicketData:
    try:
        user_id_from_token_str = current_user.get("sub")

        print(f"DEBUG: User ID received from frontend (token): {user_id_from_token_str}")

        if not user_id_from_token_str:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID not found in token payload."
            )

        try:
            user_id_from_token = uuid.UUID(user_id_from_token_str)
            print(f"DEBUG: Converted user_id_from_token to UUID: {user_id_from_token}")
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        response = supabase.table('ticket_booking').select("*").eq('id', ticket_id).single().execute()

        
        ticket_data = response.data
        owner_id_str = ticket_data.get("user_id")
        print(f"DEBUG: Ticket Owner ID from database: {owner_id_str}") 

        try:
            owner_id = uuid.UUID(owner_id_str)
            print(f"DEBUG: Converted owner_id from database to UUID: {owner_id}") 
        except ValueError:
            pass 

        if owner_id != user_id_from_token:
            print(f"DEBUG: Mismatch! Token user_id: {user_id_from_token}, Ticket owner_id: {owner_id}") # Add this for specific debug
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource."
            )
        return TicketData(**ticket_data)

    except HTTPException:
        raise
    except Exception as e:
        print(f"An unexpected error occurred while fetching ticket {ticket_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )