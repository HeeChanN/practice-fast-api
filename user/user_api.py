from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from user.user_schema import CreateUserForm, UserAuth
from database import get_db
from fastapi.responses import JSONResponse
from user import user_service

from jose import jwt
import os
from datetime import timedelta, datetime
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

app = APIRouter(prefix="/api/user")


@app.post("/signup",summary="회원 가입")
async def create_user_api(
    new_user: CreateUserForm, db: Session = Depends(get_db)
):
    if user_service.create_user(new_user,db) == False:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="중복 생성")
    
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "회원 가입 완료"})


@app.post("/login")
async def login_api(form_data: UserAuth,
                    db: Session = Depends(get_db)):
    user = user_service.get_user(form_data.email, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    
    response = user_service.verify_password(form_data.password, user.password)
    if not response:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="잘못된 아이디 혹은 비밀번호")
    
    data = {
        "sub": user.email,
        "exp": datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    }
    
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "email": user.email,
        "name": user.name
    }