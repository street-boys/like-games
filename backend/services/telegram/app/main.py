from asyncio import run

from aiogram import Dispatcher, Bot

from api import api_router
from core.config import get_telegram_settings
from core.tools import store


def create_bot() -> Bot:
    _bot = Bot(token=get_telegram_settings().TELEGRAM_BOT_API_TOKEN, parse_mode="HTML")
    return _bot


def create_dispatcher() -> Dispatcher:
    _dispatcher = Dispatcher()
    _dispatcher.include_router(api_router)

    _dispatcher.startup.register(store.connect)
    _dispatcher.shutdown.register(store.disconnect)

    return _dispatcher


async def main() -> None:
    bot = create_bot()
    dp = create_dispatcher()

    await dp.start_polling(bot)


if __name__ == "__main__":
    run(main())
