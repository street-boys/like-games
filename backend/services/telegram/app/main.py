from aiogram import Dispatcher

from core.tools import store
from misc.dp import dp
from misc.bot import bot

from handlers.private import private_router

dp.include_router(private_router)


async def startup(dispatcher: Dispatcher) -> None:
    await store.connect()


async def shutdown(dispatcher: Dispatcher) -> None:
    await store.disconnect()


if __name__ == '__main__':
    dp.run_polling(bot)
    #start_polling(dispatcher=dp, skip_updates=True, on_startup=startup, on_shutdown=shutdown)
