from models.BusStop import BusStop
from sqlalchemy.orm import Session
from typing  import List
from exceptions import BusStopNotFoundError

def get_bus_stop_by_route_id(route_id: str, db_session: Session) -> List[BusStop]:

    bus_stop : List[BusStop] | None = db_session.query(BusStop).filter(BusStop.route_id == route_id).all()
    if bus_stop == None:
        raise BusStopNotFoundError("Bus stop not found")
    
    return bus_stop