from sqlalchemy import Column, Integer, VARCHAR, DateTime
from datetime import datetime
from database import Base

class User(Base):
    __tablename__="User"
    
    no = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(15), nullable=False)
    email = Column(VARCHAR(20), nullable=False)
    password = Column(VARCHAR(20), nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.now)
    