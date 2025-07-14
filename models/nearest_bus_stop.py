from pydantic import BaseModel
from typing import List

class BusStopPathResponse(BaseModel):
    name: str
    latitude: float
    longitude: float
    distance: float  
    duration: float
    coordinates: List[List[float]]  

class NearestBusStopResponse(BusStopPathResponse):
    pass

class BusStopPathRequest(BaseModel):
    user_longitude: float
    user_latitude:float
    longitude: float
    latitude: float

class NearestBusStopRequest(BaseModel):
    longitude: float
    latitude: float
    route_id: str
    
