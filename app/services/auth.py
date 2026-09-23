from pydantic import EmailStr
from sqlmodel import select
from fastapi import HTTPException, status
from app.core.database import SessionDP
from app.core.security import blacklist_token, create_token, hash_password, verify_password, verify_token
from app.models.models import User
from sqlmodel.ext.asyncio.session import AsyncSession



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

    return {"message" : "Registration Successfull!"}


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