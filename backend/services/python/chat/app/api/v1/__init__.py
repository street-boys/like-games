from fastapi import APIRouter

from api.v1.routers.chat import chat_router
from api.v1.routers.message import message_router
from api.v1.routers.users import users_router
from api.v1.ws.chat import ws_chat_router

v1_router = APIRouter()
v1_router.include_router(chat_router)
v1_router.include_router(message_router)
v1_router.include_router(users_router)
v1_router.include_router(ws_chat_router)
