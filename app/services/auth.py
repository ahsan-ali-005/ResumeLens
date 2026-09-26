from pydantic import EmailStr
from sqlmodel import select
from fastapi import HTTPException, status
from app.core.database import SessionDP
from app.core.security import blacklist_token, create_token, create_verification_token, hash_password, verify_password, verify_token, verify_verification_token
from app.models.models import User
from sqlmodel.ext.asyncio.session import AsyncSession

from app.schemas.schemas import ResetPasswordRequest
from app.services.email import send_confirmation_email_service, send_password_reset_email_service



async def register_user_service(data,session):
    query = select(User).where(User.email == data.email)
    result = await session.exec(query)
    existing_user = result.first()

    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User Already Exists!")
    
    hashed_password = hash_password(data.password)

    user = User(
        name=data.name,
        email=data.email,
        password_hash=hashed_password
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    token = create_verification_token(data.email)
    await send_confirmation_email_service(name=data.name, email=data.email, token=token)

    return {"message" : "Registration Successfull! Please Verify your Email!"}
    


async def login_user_service(email: str, password: str, session: AsyncSession):

    query = await session.exec(select(User).where(User.email == email))
    user = query.first()

    if user and verify_password(plain_password=password, hashed_password=user.password_hash):
        token = create_token({"sub":email})
        return {"message": "Login Success" ,"access_token": token, "token_type": "bearer"}

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong Email or password!")


async def logout_user_service(token):

    payload = verify_token(token)
    exp = payload.get("exp")
    blacklist_token(token,exp)
    return {"message" : "User Logout!"}


async def verify_email_service(token: str, session: AsyncSession):

    email = verify_verification_token(token=token)
    query = select(User).where(User.email == email)
    result = await session.exec(query)
    user = result.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not Registered.")

    if user.is_verified:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is already verified!")

    user.is_verified = True
    await session.commit()
    return {"message" : "Email Verified Successfully!"}


async def forgot_password_service(email: EmailStr, session: AsyncSession):

    query = select(User).where(User.email == email)
    result = await session.exec(query)
    user = result.first()

    if user:
        token = create_token(email)
        await send_password_reset_email_service(name=user.name, email=email, token=token)
        return {"message" : "If you are registered you got the password reset email. Check your Inbox!"}


async def password_reset_service(data: ResetPasswordRequest, session: AsyncSession):
    email = verify_verification_token(token=data.token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid or expired token."
        )

    query = select(User).where(User.email == email)
    result = await session.exec(query)
    user = result.first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found."
        )

    user.hashed_password = hash_password(data.new_password)
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return {"message": "Password has been reset successfully."}