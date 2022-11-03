from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.v1.routers.cookie import cookie_router
from api.v1.routers.oauth2 import oauth2_router
from core.depends import get_session
from core.tools import store
from orm.user import UserModel
from responses.okay import okay_response
from schemas.user import UserRegistrationSchema, UserSchema
from utils.auth import get_password_hash

v1_router = APIRouter()
v1_router.include_router(cookie_router)
v1_router.include_router(oauth2_router)


@v1_router.post(path=".registration", status_code=status.HTTP_201_CREATED)
async def registration(
    user_data: UserRegistrationSchema, session: AsyncSession = Depends(get_session)
) -> dict:
    user = await store.user_accessor.get_user_by(
        session=session, where=(UserModel.email == user_data.email)
    )
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"user with {user.email=} already exits",
        )

    _, __, password_len = map(lambda k: len(k[1]), user_data)

    if password_len < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"password length must be greater than 8, got {password_len=}",
        )

    hashed_password = get_password_hash(user_data.password)

    user = await store.user_accessor.create_user(
        session=session,
        email=user_data.email,
        username=user_data.username,
        password=hashed_password,
    )

    user_out = UserSchema.from_orm(user)

    return okay_response(detail={"user": user_out.dict()})
