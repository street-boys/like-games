from store.aiohttp_session.accessor import SessionAccessor
from store.integration import IntegrationPotAccessor, IntegrationUserAccessor


class Store:
    def __init__(self) -> None:
        self.aiohttp_accessor = SessionAccessor()
        self.integration_pot_accessor = IntegrationPotAccessor()
        self.integration_user_accessor = IntegrationUserAccessor()

    async def connect(self) -> None:
        await self.aiohttp_accessor.connect()

    async def disconnect(self) -> None:
        await self.aiohttp_accessor.disconnect()
