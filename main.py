from fastapi import Depends, FastAPI, Request
from fastapi.responses import StreamingResponse
from time import sleep
from fastapi.middleware.cors import CORSMiddleware
import random
import json
from bus_location import loc_list
from pydantic import BaseModel

app = FastAPI()

class OwnTracksLocation(BaseModel):
    _type: str
    tid: str
    lat: float
    lon: float
    tst: int
    batt: int

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

def event_generator(route_id: str):
    route_locs = loc_list.get(route_id)
    if not route_locs:
        yield f"event: error\ndata: Route '{route_id}' not found\n\n"
        return

    for loc in route_locs:
        event_data = {
            "lat": loc[0],
            "lng": loc[1],
        }
        yield f"data: {json.dumps(event_data)}\n\n"
        sleep(3)

    yield f"event: done\ndata: Broadcast completed for route {route_id}, total {len(route_locs)} points\n\n" 

@app.get("/stream/{route_id}")
async def stream_route(route_id: str):
    return StreamingResponse(
        event_generator(route_id),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache"}
    )


# @app.get("/gpsloc")
# async def get_loc(request : Request):

#     body = await request.json()

#     if body.get("_type") == "location":
#         bus_id = body.get("tid", "unknown")
#         lat = body.get("lat")
#         lon = body.get("lon")
#         timestamp = body.get("tst")
#         battery = body.get("batt", None)

#         print(f"[{bus_id}] Lat: {lat}, Lon: {lon}, Time: {timestamp}, Battery: {battery}")
#     else:
#         print("Non-location payload received:", body)

#     return {"status": "ok"}

