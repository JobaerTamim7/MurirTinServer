from crud.Bus.get_bus import get_bus_stop_by_route_id
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from typing import List
from schemas.BusStopSchema import BusStopResponse
from models.BusStop import BusStop

def get_all_buses_by_route(route_id: str, db_session: Session):
    try:
        buses : List[BusStop] = get_bus_stop_by_route_id(route_id, db_session)

        if len(buses) == 0:
            return JSONResponse(content={"detail": "No buses found for this route"}, status_code=404)
        
        response = [
            BusStopResponse(name=bus.name, latitude=bus.latitude, longitude=bus.longitude) for bus in buses
        ]

        return response
    except Exception as e:
        return JSONResponse(content={"detail": "An unexpected error occurred", "error": str(e)}, status_code=500)
    