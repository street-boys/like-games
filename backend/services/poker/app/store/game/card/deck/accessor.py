from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload

from orm import DeckModel
from store.base import BaseAccessor


class DeckAccessor(BaseAccessor):
    async def create_deck(self, session: AsyncSession) -> DeckModel:
        to_return = DeckModel()

        session.add(to_return)

        return to_return

    async def insert_cards(self, session: AsyncSession, deck_id: int) -> None:
        joinedload()
        deck = await session.execute(
            select(DeckModel).
            where(DeckModel.id == deck_id).options
        )
