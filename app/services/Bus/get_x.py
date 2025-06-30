from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from typing import List
from schemas.BusStopSchema import BusStopResponse
from models.BusStop import BusStop

def get_all_buses_by_route(route_id: str, db_session: Session):
    try:
        bus_stops : List[BusStop] | None = db_session.query(BusStop).filter(BusStop.route_id == route_id).order_by(BusStop.order.asc()).all()

        if len(bus_stops) == 0:
            return JSONResponse(content={"detail": "No buses found for this route"}, status_code=404)
        
        response = [
            BusStopResponse(name=bus_stop.name, latitude=bus_stop.latitude, longitude=bus_stop.longitude) for bus_stop in bus_stops
        ]

        return response
    except Exception as e:
        return JSONResponse(content={"detail": "An unexpected error occurred", "error": str(e)}, status_code=500)
    
def get_all_routes(db_session: Session):
    try:
        routes =  db_session.query(BusStop.route_id).distinct().all() 


        if not routes:
            return JSONResponse(content={"detail": "No routes found"}, status_code=404)
        
        route_ids = [str(route[0]) for route in routes] 

        return route_ids
    except Exception as e:
        return JSONResponse(content={"detail": "An unexpected error occurred", "error": str(e)}, status_code=500)