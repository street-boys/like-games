from fastapi import APIRouter

from api.v1.routers.profile import profile_router

v1_router = APIRouter()
v1_router.include_router(profile_router)
