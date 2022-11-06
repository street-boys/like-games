from aiogram import Router, types
from aiogram.filters import Command

from core.tools import store

router = Router()


@router.message(Command(commands=["pot"]))
async def pot(message: types.Message) -> None:
    user = await store.integration_user_accessor.get_user_by_telegram(
        telegram=message.from_user.id
    )
    user_pot = await store.integration_pot_accessor.get_user_pot(user_id=user.id)

    await message.answer(
        f"@{message.from_user.username}, you have <b>{user_pot.pot}</b> chips on balance."
    )
