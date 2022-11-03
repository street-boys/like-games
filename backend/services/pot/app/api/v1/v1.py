from fastapi import APIRouter

from api.v1.routers.pot import pot_router

v1_router = APIRouter()
v1_router.include_router(pot_router)
