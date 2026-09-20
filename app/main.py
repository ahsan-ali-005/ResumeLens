from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import create_db_tables


@asynccontextmanager
async def lifespan_handler(app : FastAPI):
    await create_db_tables()
    print("Tables Created Successfully!")
    yield


app = FastAPI(lifespan=lifespan_handler)



@app.get("/")
def home():
    return {"message": "Welcome to ResumeLens API"}