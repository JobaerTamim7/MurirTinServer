from fastapi import HTTPException, status
from database import supabase 
from models.ticket import BookTicketRequest, TicketBookingResponse
from datetime import datetime
from typing import Optional

async def book_tickets(
    request: BookTicketRequest,
    current_user: dict 
) -> TicketBookingResponse:
   
    from_loc = request.from_location.strip()
    to_loc = request.to_location.strip()
    ticket_count = request.ticket_count
    user_id = current_user.get("sub") 

    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required for booking.")

    
    if not from_loc or not to_loc or ticket_count <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if ticket_count > 4:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    try:

        route_response = supabase.table('bus_routes').select('price, id, available_seats').ilike('from_location', from_loc).ilike('to_location', to_loc).limit(1).execute()

        if not route_response.data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bus route not found for the given locations.")

        route_data = route_response.data[0]
        available_seats = route_data.get('available_seats')
        price = route_data.get('price')
        route_id = route_data.get('id')

        if available_seats is None or price is None or route_id is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        
        if ticket_count > available_seats:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        total_cost = ticket_count * price

        booking_insert_data = {
            'route_id': route_id,
            'from_location': from_loc,
            'to_location': to_loc,
            'ticket_count': ticket_count,
            'total_cost': total_cost,
            'booking_time': datetime.now().isoformat(),
            'user_id': user_id 
        }
        booking_response = supabase.table('ticket_booking').insert(booking_insert_data).execute()

        if not booking_response.data:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to insert booking into database.")

        booking_record = booking_response.data[0]
        booking_id = booking_record.get('id', 'N/A')

        update_response = supabase.table('bus_routes').update({'available_seats': available_seats - ticket_count}).eq('id', route_id).execute()

        if not update_response.data:
            
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update available seats after booking.")

        
        return TicketBookingResponse(
            message="Ticket booked successfully!",
            ticket_count=ticket_count,
            total_cost=total_cost,
            booking_id=str(booking_id)
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"An unexpected error occurred during ticket booking: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )