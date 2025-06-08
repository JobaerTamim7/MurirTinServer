from fastapi import FastAPI
from typing import Dict
from api.Auth.router import auth_router
import uvicorn

app : FastAPI = FastAPI()
app.include_router(auth_router)

def main():
    uvicorn.run('main:app',reload=True)

if __name__ == '__main__':
    main()