# main.py
from fastapi import FastAPI, Depends
from routers import auth, ticket, signup, profile, complaint
from utils.jwt_token import get_current_user

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(signup.router)
app.include_router(profile.router)
app.include_router(complaint.router)

@app.get("/")
async def root():
    return {"message": "API is running gastly"}

# @app.get("/protected/")
# async def protected_route(current_user: dict = Depends(get_current_user)):
#     return {"message": "This is a protected route", "user": current_user}