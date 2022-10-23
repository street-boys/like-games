from fastapi import APIRouter

from api.v3.routers.update import update_router

v3_router = APIRouter()
v3_router.include_router(update_router)
