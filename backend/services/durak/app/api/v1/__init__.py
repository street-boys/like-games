from fastapi import APIRouter

from api.v1.routers.card import card_router
from api.v1.routers.game import game_router
from api.v1.routers.users import users_router

v1_router = APIRouter()
v1_router.include_router(card_router)
v1_router.include_router(game_router)
v1_router.include_router(users_router)
