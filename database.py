from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv



load_dotenv()
DB_URL = os.getenv("DATABASE_URL")


engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() # 객체와 테이블 매핑

# 세션을 생성하여 db 관련 작업을 수행할 수 있도록 도와주고 끝에는 세션을 close() 하는 메서드
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        