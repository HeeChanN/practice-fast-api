from fastapi import Header, Depends
from database import get_db
from user import user_service

def get_current_user(token: str = Header(...), db : Session = Depends(get_db)):
    try:
        user_email = user_service.ve