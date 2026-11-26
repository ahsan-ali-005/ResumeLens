from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.models import User


async def get_user_by_email(email: str, session: AsyncSession) -> User | None:
    result = await session.exec(select(User).where(User.email == email))
    return result.first()