from sqlalchemy.ext.asyncio import AsyncSession

from db.session import session


async def get_session() -> AsyncSession:
    async with session.begin() as s:
        yield s
