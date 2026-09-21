from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import create_db_tables
from app.routers.auth import router as auth_router

@asynccontextmanager
async def lifespan_handler(app : FastAPI):
    await create_db_tables()
    yield


app = FastAPI(lifespan=lifespan_handler)
app.include_router(auth_router)



@app.get("/")
def home():
    return {"message": "Welcome to ResumeLens API"}