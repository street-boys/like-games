from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from starlette import status

from accessors.user import create_user, get_user_by
from api.v1.routers.cookie import cookie_router
from orm.user import user_schema_in_registration, user_schema_out
from responses.okay import okay_response
from structures.enums import FilterEnum
from structures.named_tuples import attribute
from utils.auth import get_password_hash

v1_router = APIRouter()
v1_router.include_router(cookie_router)


@v1_router.post(path='.registration',
                status_code=status.HTTP_201_CREATED)
async def registration(user_data: user_schema_in_registration) -> dict:
    user = await get_user_by(attr=attribute(filter=FilterEnum.email), value=user_data.email)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'user with {user.email=} already exits')

    _, __, password_len = map(lambda k: len(k[1]), user_data)

    if password_len < 8:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'password length must be greater than 8, got {password_len=}')

    hashed_password = get_password_hash(user_data.password)

    user = await create_user(email=user_data.email,
                             username=user_data.username,
                             password=hashed_password)

    user_out = await user_schema_out.from_tortoise_orm(user)

    return okay_response(detail={
        'user': user_out.dict()
    })
