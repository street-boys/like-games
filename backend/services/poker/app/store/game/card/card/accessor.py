from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from orm.card import CardModel
from schemas.game import CardSchema


class CardAccessor:
    async def create_card(self, session: AsyncSession, card: CardSchema) -> CardModel:
        to_return = CardModel(rank=card.rank, suit=card.suit)

        session.add(to_return)

        return to_return

    async def get_card_by(self, session: AsyncSession, where: Any) -> CardModel:
        to_return = await session.execute(select(CardModel).where(where))

        return to_return.scalar()
