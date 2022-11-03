from aiogram import Router
from aiogram.types import Message

from accessors.integration.pot import get_user_pot
from accessors.integration.users import get_user_telegram

pot_router = Router()


@pot_router.message(commands=['pot'])
async def pot_message_handler(message: Message) -> None:
    user = await get_user_telegram(message.from_user.id)

    pot = await get_user_pot(user_id=user.id)

    await message.answer(f'@{user.username}, you have **{pot.pot}** chips on balance')
