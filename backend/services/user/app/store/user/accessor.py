from typing import Any

from pydantic import EmailStr
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from orm.user import UserModel
from structures.enums import RegistrationTypeEnum


class UserAccessor:
    async def create_user(
        self, session: AsyncSession, email: EmailStr, username: str, password: str
    ) -> UserModel:
        to_return = UserModel(email=email, username=username, password=password)

        session.add(to_return)

        return to_return

    async def create_user_telegram(
        self, session: AsyncSession, telegram: int, username: str
    ) -> UserModel:
        to_return = UserModel(
            telegram=telegram, username=username, registration_type=RegistrationTypeEnum.telegram
        )

        session.add(to_return)

        return to_return

    async def update_user(self, session: AsyncSession, user_id: int, values: dict) -> None:
        await session.execute(update(UserModel).where(UserModel.id == user_id).values(**values))

    async def get_user_by(self, session: AsyncSession, where: Any) -> UserModel:
        to_return = await session.execute(select(UserModel).where(where))

        return to_return.scalar()
