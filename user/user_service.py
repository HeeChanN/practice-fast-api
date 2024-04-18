from sqlalchemy.orm import Session

from models import User
from user.user_schema import CreateUserForm
from passlib.context import CryptContext


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



# 단일 유저 조회
def get_user(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()

# 비밀번호 검증
def verify_password(password, hash_password):
    return pwd_context.verify(password, hash_password)
