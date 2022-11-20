from .aiohttp_session.accessor import SessionAccessor
from .game.card import CardAccessor, DeckAccessor
from .game.logic import LogicDeckAccessor
from .game.player import PlayerAccessor, UserAccessor
from .integration import IntegrationUserAccessor


class Store:
    def __init__(self) -> None:
        self.aiohttp_accessor = SessionAccessor(self)
        self.card_accessor = CardAccessor(self)
        self.deck_accessor = DeckAccessor(self)
        self.logic_deck_accessor = LogicDeckAccessor(self)
        self.player_accessor = PlayerAccessor(self)
        self.user_accessor = UserAccessor(self)
        self.integration_user_accessor = IntegrationUserAccessor(self)

    async def connect(self) -> None:
        await self.aiohttp_accessor.connect()

    async def disconnect(self) -> None:
        await self.aiohttp_accessor.disconnect()
