from fastapi import HTTPException
from typing import List,Dict
from models.bus_stop import BusStopResponse
from database import supabase
from postgrest.base_request_builder import APIResponse
import httpx
from models.nearest_bus_stop import NearestBusStopResponse
from geopy.distance import geodesic

def get_all_bus_stops_by_route_id(route_id: str):
    try:
        response : APIResponse = supabase\
            .table("bus_stops")\
            .select("name, latitude, longitude")\
            .eq("route_id", route_id)\
            .order("order",desc=False)\
            .execute()
        data : List[Dict] = response.data 
        if len(data) == 0 or data is None:
            raise HTTPException(
                status_code=404, 
                detail="No bus stops found for the given route ID."
                )
        
        bus_stops: List[BusStopResponse] = [
            BusStopResponse(name=item["name"],
                            latitude=float(item["latitude"]),
                            longitude=float(item["longitude"])) for item in data
            ]
        return bus_stops
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while fetching bus stops: {str(e)}"
        )
    
def get_all_routes():
    try:
        response : APIResponse = supabase\
            .table("bus_stops")\
            .select("route_id")\
            .execute()
        
        data : List[Dict] = response.data
        if len(data) == 0 or data is None:
            raise HTTPException(
                status_code=404, 
                detail="No routes found."
            )
        routes : List[str] = list(set([str(item["route_id"]) for item in data]))
        return routes
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while fetching routes: {str(e)}"
        )
    
async def get_nearest_bus_stop(longitude: float, latitude: float, route_id: str):
    try:
        bus_stops : List[BusStopResponse] = get_all_bus_stops_by_route_id(route_id)

        min_distance : float = float('inf')
        nearest_bus_stop : BusStopResponse = bus_stops[0]

        for bus_stop in bus_stops:
            bus_stop_location = (bus_stop.latitude, bus_stop.longitude)
            user_location = (latitude, longitude)
            distance = geodesic(user_location, bus_stop_location).meters
            
            if distance < min_distance:
                min_distance = distance
                nearest_bus_stop = bus_stop


        url : str = f"https://api.mapbox.com/directions/v5/mapbox/walking/{longitude},{latitude};{nearest_bus_stop.longitude},{nearest_bus_stop.latitude}?alternatives=false&continue_straight=true&geometries=geojson&overview=full&steps=false&access_token=pk.eyJ1IjoidGFtaW03IiwiYSI6ImNtYzByY243djA2Y2UybHIydTllaHhudjIifQ.6zTjpL0hMo0oQWBt8KNHOQ"

        data = dict()
        async with httpx.AsyncClient() as client:
            response = await client.get(url=url)
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail="Failed to fetch directions from Mapbox API."
                )
            data = response.json()

        coordinates = data["routes"][0]["geometry"]["coordinates"]

        nearest_bus_stop_response = NearestBusStopResponse(
            name=nearest_bus_stop.name,
            latitude=nearest_bus_stop.latitude,
            longitude=nearest_bus_stop.longitude,
            distance=data["routes"][0]["distance"],
            duration=data["routes"][0]["duration"],
            coordinates=coordinates
        )

        return nearest_bus_stop_response
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while fetching the nearest bus stop: {str(e)}"
        )
