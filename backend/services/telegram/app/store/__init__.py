from store.aiohttp_session.session import Session


class Store:
    def __init__(self) -> None:
        self.aiohttp_accessor = Session()

    async def connect(self) -> None:
        await self.aiohttp_accessor.connect()

    async def disconnect(self) -> None:
        await self.aiohttp_accessor.disconnect()
