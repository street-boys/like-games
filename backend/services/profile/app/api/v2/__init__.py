from fastapi import APIRouter

from api.v2.routers.view import view_router

v2_router = APIRouter()
v2_router.include_router(view_router)
