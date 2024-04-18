from sqlalchemy.orm import Session

from models import User
from user.user_schema import CreateUserForm,UserAuth
from passlib.context import CryptContext

from jose import jwt
import os
from datetime import timedelta, datetime
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

# 회원가입
def create_user(new_user: CreateUserForm, db: Session):
    
    checkUser = get_user(new_user.email, db)
    if checkUser:
        return False
    user = User(
        userId = new_user.userId,
        email = new_user.email,
        name = new_user.name,
        password = pwd_context.hash(new_user.password),
        phoneNo = new_user.phoneNo 
    )
    
    db.add(user)
    db.commit()
    return True

# 로그인 검증
def verify_user_info(form_data: UserAuth, db: Session):
    
    # 검증
    check_user = get_user(form_data.userId, db)
    if not check_user:
        return False
    if not pwd_context.verify(form_data.password, check_user.password):
        return False
    
    # Response 발급
    data = {
        "sub": check_user.userId,
        "exp": datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    }
    
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "email": check_user.userId,
        "name": check_user.name
    }

# 단일 유저 조회
def get_user(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()
