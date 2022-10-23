from fastapi import APIRouter

from api.v1 import v1_router
from api.v2 import v2_router

api_router = APIRouter()
api_router.include_router(v1_router, tags=['v1'])
api_router.include_router(v2_router, tags=['v2'])
