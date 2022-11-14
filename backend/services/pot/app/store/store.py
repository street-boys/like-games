from .aiohttp_session.accessor import SessionAccessor
from .integration import IntegrationUserAccessor
from .pot.accessor import PotAccessor


class Store:
    def __init__(self) -> None:
        self.aiohttp_accessor = SessionAccessor()
        self.integration_user_accessor = IntegrationUserAccessor()
        self.pot_accessor = PotAccessor()

    async def connect(self) -> None:
        await self.aiohttp_accessor.connect()

    async def disconnect(self) -> None:
        await self.aiohttp_accessor.disconnect()
