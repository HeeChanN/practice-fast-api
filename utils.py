import jwt
from fastapi import HTTPException, Security,Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta

from fastapi.security import HTTPAuthorizationCredentials
import os
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# jwt 생성
def create_access_token(userId: str):
    
    data = {
        "sub": userId,
        "exp": datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    }
    
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# jwt 해독
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return False

security = HTTPBearer()

# 토큰 검증 및 유저 id 추출
def verify_token(info: HTTPAuthorizationCredentials = Depends(security)):
    token = info.credentials
    payload = decode_access_token(token)
    if payload == False:
        raise HTTPException(status_code=401, detail="로그인을 하고 진행해 주세요.")
    userId = payload.get("sub")
    return userId