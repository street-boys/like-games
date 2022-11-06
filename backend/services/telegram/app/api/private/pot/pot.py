from aiogram import Router, types
from aiogram.filters import Command

pot_router = Router()


@pot_router.message(Command(commands=['pot']))
async def pot(message: types.Message) -> None:
    user
