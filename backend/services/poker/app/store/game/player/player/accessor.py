from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from orm import PlayerModel, UserModel
from store.base import BaseAccessor


class PlayerAccessor(BaseAccessor):
    async def create_player(self, session: AsyncSession, user: UserModel) -> PlayerModel:
        exists = await self.get_player_by(session=session, where=(UserModel.id == user.id))
        if exists:
            return exists

        to_return = PlayerModel(user=user)

        session.add(to_return)

        return to_return

    async def get_player_by(self, session: AsyncSession, where: Any) -> PlayerModel:
        to_return = await session.execute(
            select(PlayerModel).where(where).options(joinedload(PlayerModel.user))
        )

        return to_return.scalar()
