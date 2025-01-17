from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from user.user_schema import CreateUserForm, UserAuth, UserResponse
from database import get_db
from fastapi.responses import JSONResponse
from user import user_service
from utils import verify_token

app = APIRouter(prefix="/api/user")


@app.post("/signup",summary="회원 가입")
async def create_user_api(new_user: CreateUserForm, db: Session = Depends(get_db)):
    if user_service.create_user(new_user,db) == False:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="중복 생성")
    
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "회원 가입 완료"})


@app.post("/login", summary="로그인")
async def login_api(form_data: UserAuth, db: Session = Depends(get_db)):
    
    
    response = user_service.verify_user_info(form_data, db)
    if response == False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="잘못된 아이디 혹은 비밀번호")

    return response

@app.get("/userInfo", summary="내정보 조회")
async def get_user_info(userId: str = Depends(verify_token),db: Session = Depends(get_db)):
    
    user = user_service.get_user(userId, db)
    return UserResponse(
        userId = user.userId,
        email = user.email,
        name = user.name,
        phoneNo = user.phoneNo 
    )