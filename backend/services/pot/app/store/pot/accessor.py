from typing import Any

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from orm.pot import PotModel


class PotAccessor:
    async def create_pot(self, session: AsyncSession, user_id: int) -> PotModel:
        to_return = PotModel(user_id=user_id)

        session.add(to_return)

        return to_return

    async def update_pot(
        self,
        session: AsyncSession,
        pot_id: int,
        pot: int,
    ) -> None:
        await session.execute(update(PotModel).where(PotModel.id == pot_id).values(pot=pot))

    async def get_pot_by(self, session: AsyncSession, where: Any) -> PotModel:
        to_return = await session.execute(select(PotModel).where(where))

        return to_return.scalar()
