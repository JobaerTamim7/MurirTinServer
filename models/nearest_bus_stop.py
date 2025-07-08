from pydantic import BaseModel
from typing import List

class NearestBusStopResponse(BaseModel):
    name: str
    latitude: float
    longitude: float
    distance: float  
    duration: float
    coordinates: List[List[float]]  

class NearestBusStopRequest(BaseModel):
    longitude: float
    latitude: float
    route_id: str
    
