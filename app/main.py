from fastapi import FastAPI
from typing import Dict

app : FastAPI = FastAPI()
@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@app.get('/greet/{name}')
async def greet_name(name : str) -> Dict[str, str]:
    return {"message": f"Hello, {name}!"}

@app.get('/greet1')
async def greet1(name: str) -> Dict[str, str]:
    return {"message": f"Hello, {name}!"}