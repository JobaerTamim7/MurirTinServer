from fastapi import HTTPException, status
from database import supabase 
from models.ticket import BookTicketRequest, TicketBookingResponse
from datetime import datetime
from typing import Optional
import requests

async def book_tickets(
    request: BookTicketRequest,
    current_user: dict 
) -> TicketBookingResponse:
   
    from_loc_position = (request.from_location_long, request.from_location_lat)
    to_loc_position = (request.to_location_long, request.to_location_lat)
    ticket_count = request.ticket_count
    user_id = current_user.get("sub") 

    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required for booking.")


    if ticket_count > 4:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    try:

        mapbox_directions_url = f"https://api.mapbox.com/directions/v5/mapbox/driving/{from_loc_position[0]},{from_loc_position[1]};{to_loc_position[0]},{to_loc_position[1]}?alternatives=false&annotations=distance&geometries=geojson&language=en&overview=full&steps=true&access_token=pk.eyJ1IjoidGFtaW03IiwiYSI6ImNtYzByY243djA2Y2UybHIydTllaHhudjIifQ.6zTjpL0hMo0oQWBt8KNHOQ"
        response = requests.get(mapbox_directions_url)

        data = response.json()


        rounded_price = 0

        if response.status_code == 200 and "routes" in data and data["routes"]:
            total_distance = data["routes"][0]["distance"]
            distance_km = total_distance/1000
            rate = 5

            price = distance_km * rate
            rounded_price = price // 5 + 5

        


        total_cost = ticket_count * rounded_price

        booking_insert_data = {
            'route_id': request.route_id,
            'from_location': request.from_location,
            'to_location': request.to_location,
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