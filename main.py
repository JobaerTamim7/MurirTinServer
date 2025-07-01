from fastapi import FastAPI, Depends
from routers import auth, ticket, signup, profile, complaint,ticket, qr_code
from utils.jwt_token import get_current_user

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(signup.router)
app.include_router(profile.router)
app.include_router(complaint.router)
app.include_router(ticket.router)
app.include_router(qr_code.router)

@app.get("/")
async def root():
    return {"message": "API is running successfully!"}

