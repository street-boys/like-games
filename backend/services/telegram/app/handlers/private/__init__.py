from aiogram import types
from aiogram import Router
from aiogram.filters import Command

from core.middlewares import PrivateChatMiddleware

private_router = Router()
private_router.message.middleware(PrivateChatMiddleware())


@private_router.message(Command(commands=['lol']))
async def some(message: types.Message) -> None:
    await message.send_copy(chat_id=message.chat.id)
