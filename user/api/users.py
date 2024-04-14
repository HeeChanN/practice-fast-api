from sqlalchemy.orm import Session
from database import get_db
from fastapi import APIRouter

app = APIRouter(prefix="/user")

@app.get("/test")
async def board_test():
    return "test"