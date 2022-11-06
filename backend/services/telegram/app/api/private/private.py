from aiogram import Router

from api.private.pot.pot import router as pot_router

private_router = Router()
private_router.include_router(pot_router)
