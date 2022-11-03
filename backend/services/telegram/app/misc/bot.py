from aiogram import Bot

from core.config import get_telegram_settings

bot = Bot(token=get_telegram_settings().TELEGRAM_BOT_API_TOKEN, parse_mode='html')
