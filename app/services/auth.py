from sqlmodel import select
from fastapi import HTTPException, status
from app.core.database import SessionDP
from app.core.security import hash_password
from app.models.models import User





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


async def login_user():
    pass