from fastapi import APIRouter, status
from typing import List
from models.bus_stop import BusStopResponse
from models.nearest_bus_stop import NearestBusStopResponse,NearestBusStopRequest
from services.Bus.get_x import get_all_bus_stops_by_route_id
from services.Bus.get_x import get_all_routes
from services.Bus.get_x import get_nearest_bus_stop
from utils.jwt_token import get_current_user
from fastapi import Depends

bus_router = APIRouter(prefix="/bus",tags=["bus"])

@bus_router.get("/bus_stop/{route_id}", response_model=List[BusStopResponse],status_code=status.HTTP_200_OK)
async def bus_stops_by_id(route_id: str, current_user: dict = Depends(get_current_user)):
    response = get_all_bus_stops_by_route_id(route_id=route_id, current_user=current_user)

    return response

@bus_router.get("/routes", response_model=List[str], status_code=status.HTTP_200_OK)
async def all_routes(current_user: dict = Depends(get_current_user)):
    response = get_all_routes(current_user=current_user)

    return response

@bus_router.post("/nearest_stop", response_model=NearestBusStopResponse, status_code=status.HTTP_200_OK)
async def nearest_bus_stop(body: NearestBusStopRequest, current_user: dict = Depends(get_current_user)):
    response = await get_nearest_bus_stop(longitude=body.longitude, latitude=body.latitude, route_id=body.route_id, current_user=current_user)

    return response