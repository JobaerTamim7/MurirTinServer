from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_session
from typing import List
from schemas.BusStopSchema import BusStopResponse
from services.Bus.get_x import get_all_buses_by_route
from services.Bus.get_x import get_all_routes

bus_router = APIRouter(prefix="/bus",tags=["bus"])

@bus_router.get("/bus_stop/{route_id}", response_model=List[BusStopResponse])
async def bus_stops_by_id(route_id: str, db_session: Session = Depends(get_session)):
    response = get_all_buses_by_route(route_id=route_id,db_session=db_session)

    return response

@bus_router.get("/routes", response_model=List[str])
async def all_routes(db_session: Session = Depends(get_session)):
    response = get_all_routes(db_session=db_session)

    return response