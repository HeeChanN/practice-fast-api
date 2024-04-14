from fastapi import FastAPI
import models
from database import engine

models.Base.metadata.create_all(bind=engine) #db 생성

from user.api import users

app = FastAPI()

app.include_router(users.app, tags=["board"])

@app.get("/")
def read_root():
    return {"Hello":"Worldv"}