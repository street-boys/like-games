from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from core.tools import store
from orm.user import UserModel
from schemas.integration.pot import PotUpdateSchema, PotSchema


async def add_bonus(session: AsyncSession, user_id: int) -> PotSchema:
    user = await store.user_accessor.get_user_by(
        session=session, where=(UserModel.user_id == user_id)
    )
    async with session.begin_nested() as nested_session:
        bonus = await store.pot_bonus_accessor.create_bonus(
            session=nested_session.session, user=user
        )
    if await store.pot_bonus_accessor.can_take_bonus_now(
        session=session, bonus_id=bonus.id
    ):
        to_update = PotUpdateSchema(pot=bonus.bonus)
        to_return = await store.integration_pot_accessor.update_pot_for_user(
            user_id=user.user_id, data=to_update
        )

        await store.pot_bonus_accessor.update_bonus(
            session=session, bonus_id=bonus.id, last_taken_bonus=datetime.utcnow()
        )

        return to_return
