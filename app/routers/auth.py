from fastapi import Depends, FastAPI, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from app.core.database import SessionDP
from app.core.security import hash_password
from app.models.models import User
from app.schemas.schemas import CreateUser
from sqlmodel import select
from app.services.auth import login_user_service, register_user_service




router = APIRouter(prefix="/auth" , tags=["Authentication"])



@router.post("/register")
async def register_user(data: CreateUser, session: SessionDP):

    result = await register_user_service(data, session)
    return result

@router.post("/login")
async def login_user(session: SessionDP , user_data: OAuth2PasswordRequestForm = Depends()):

    result = await login_user_service(email=user_data.username, password=user_data.password, session=session)
    return result
    