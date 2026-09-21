from fastapi import FastAPI, APIRouter
from app.core.database import SessionDP
from app.core.security import hash_password
from app.models.models import User
from app.schemas.schemas import CreateUser
from sqlmodel import select
from app.services.auth import register_user_service




router = APIRouter(prefix="/auth" , tags=["Authentication"])



@router.post("/register")
async def register_user(data: CreateUser, session: SessionDP):

    result = await register_user_service(data, session)
    return result
