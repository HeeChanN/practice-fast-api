from sqlalchemy import Column, Integer, VARCHAR, DateTime
from datetime import datetime
from database import Base

class User(Base):
    __tablename__="user"
    
    no = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(VARCHAR(100), nullable=False)
    email = Column(VARCHAR(100), nullable=False)
    name = Column(VARCHAR(100), nullable=False)
    password = Column(VARCHAR(255), nullable=False)
    phoneNo = Column(VARCHAR(100), nullable=False)
    createdDate = Column(DateTime, nullable=False, default=datetime.now)
    
    