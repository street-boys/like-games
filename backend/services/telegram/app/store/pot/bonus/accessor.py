from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from orm.pot.bonus import BonusModel
from orm.user import UserModel


class BonusAccessor:
    async def create_bonus(self, session: AsyncSession, user: UserModel) -> BonusModel:
        _exists = await self.get_bonus_by(
            session=session, where=(BonusModel.user == user)
        )
        if _exists:
            return _exists

        to_return = BonusModel(user=user)

        session.add(to_return)

        return to_return

    async def update_bonus(
        self, session: AsyncSession, bonus_id: int, last_taken_bonus
    ) -> None:
        await session.execute(
            update(BonusModel)
            .where(BonusModel.id == bonus_id)
            .values(last_taken_bonus=last_taken_bonus)
        )

    async def get_bonus_by(self, session: AsyncSession, where: Any) -> BonusModel:
        to_return = await session.execute(select(BonusModel).where(where))

        return to_return.scalar()

    async def can_take_bonus_now(self, session: AsyncSession, bonus_id: int) -> bool:
        _sql = await session.execute(
            select(BonusModel).where(BonusModel.id == bonus_id)
        )
        scalar = _sql.scalar()
        try:
            estimated_time_of_taking_bonus = scalar.last_taken_bonus + timedelta(
                hours=scalar.delay_hours
            )
            if estimated_time_of_taking_bonus <= datetime.utcnow():
                return True
        except TypeError as e:
            # TypeError: BonusModel.last_taken_bonus can be as NoneType
            return True
        return False
