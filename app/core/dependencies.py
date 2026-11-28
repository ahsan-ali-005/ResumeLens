import asyncio
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.services.user import get_user_by_email
from app.core.database import SessionDP
from app.core.security import verify_token
from app.models.models import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def _write_log(line: str):
    with open("file.log", "a") as f:
        f.write(line)

async def create_log(date, time, method, endpoint, status, time_taken):
    line = f"{date} {time} | {method} | {endpoint} | {status} | {time_taken}\n"
    await asyncio.to_thread(_write_log, line)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: SessionDP,
) -> User:
    payload = await verify_token(token)
    email = payload.get("sub")

    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await get_user_by_email(email=email, session=session)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user

CurrentUser = Annotated[User, Depends(get_current_user)]