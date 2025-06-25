from pydantic import BaseModel, ConfigDict

class BusStopResponse(BaseModel):
    name : str
    latitude : float
    longitude : float

    model_config = ConfigDict(from_attributes=True)