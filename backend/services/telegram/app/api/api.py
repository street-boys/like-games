from aiogram import Router

from api.private import private_router

api_router = Router()
api_router.include_router(private_router)
