from aiohttp import ClientSession
from loguru import logger


class SessionAccessor:
    session: ClientSession = None

    def __init__(self) -> None:
        ...

    async def connect(self) -> None:
        self.session = ClientSession()

    @logger.catch(exception=AttributeError)
    async def disconnect(self) -> None:
        await self.session.close()
