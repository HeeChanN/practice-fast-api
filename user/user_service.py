from sqlalchemy.orm import Session

from models import User
from user.user_schema import CreateUserForm,UserAuth
from passlib.context import CryptContext
from utils import create_access_token


pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

# 회원가입
def create_user(new_user: CreateUserForm, db: Session):
    
    checkUser = get_user(new_user.userId, db)
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
    access_token = create_access_token(check_user.userId)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "email": check_user.userId,
        "name": check_user.name
    }

# 단일 유저 조회
def get_user(userId: str, db: Session):
    return db.query(User).filter(User.userId == userId).first()
