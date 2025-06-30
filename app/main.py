from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.Bus import bus_router
import uvicorn

app : FastAPI = FastAPI()
app.include_router(bus_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def test():
    return {"message" : "Server is running at full throttle."}

def main():
    uvicorn.run('main:app',reload=True,port=8000,host='0.0.0.0')

if __name__ == '__main__':
    main()


    