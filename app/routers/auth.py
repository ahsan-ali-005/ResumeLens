from fastapi import Depends, FastAPI, APIRouter
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.core.database import SessionDP
from app.models.models import User
from app.schemas.schemas import CreateUser, ForgotPasswordRequest, ResetPasswordRequest
from sqlmodel import select
from app.services.auth import forgot_password_service, login_user_service, logout_user_service, register_user_service, verify_email_service, password_reset_service



router = APIRouter(prefix="/auth" , tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post("/register")
async def register_user(data: CreateUser, session: SessionDP):
    result = await register_user_service(data, session)
    return result


@router.post("/login")
async def login_user(session: SessionDP , user_data: OAuth2PasswordRequestForm = Depends()):
    result = await login_user_service(email=user_data.username, password=user_data.password, session=session)
    return result


@router.post("/logout")
async def logout_user(token : str = Depends(oauth2_scheme)):
    result = await logout_user_service(token)
    return result


@router.get("/verify-email")
async def verify_email(token : str, session: SessionDP):
    result = await verify_email_service(token=token, session=session)
    return result


@router.post("/forgot-password")
async def forgot_password(data: ForgotPasswordRequest, session: SessionDP):
    result = await forgot_password_service(data.email, session)
    return result


@router.post("/reset-password")
async def reset_password(data: ResetPasswordRequest, session: SessionDP):
    return await password_reset_service(data, session)