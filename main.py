from fastapi import FastAPI
import models
from database import engine

from user import user_api

models.Base.metadata.create_all(bind=engine) #db 생성


app = FastAPI()

app.include_router(user_api.app, tags=["유저"])

@app.get("/")
def read_root():
    return {"캡스톤":"씨펫"}