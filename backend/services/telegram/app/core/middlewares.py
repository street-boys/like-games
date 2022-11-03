from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message


class PrivateChatMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        super().__init__()

    async def __call__(self,
                       handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: dict[str, Any]) -> Any:
        match event.chat.type:
            case 'private':
                return await handler(event, data)
