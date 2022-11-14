from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.depends import get_session
from core.tools import store
from orm.user import UserModel
from schemas.user import UserRegistrationSchema, UserSchema
from utils.auth import get_password_hash

from .routers.cookie import router as cookie_router
from .routers.oauth2 import router as oauth2_router
from .routers.telegram import router as telegram_router

router = APIRouter()
router.include_router(cookie_router)
router.include_router(oauth2_router)
router.include_router(telegram_router)


@router.post(
    path=".registration",
    response_description="The user on successful registration",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
)
async def registration(
    user_data: UserRegistrationSchema, session: AsyncSession = Depends(get_session)
) -> UserSchema:
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

    async with session.begin_nested() as nested_session:
        user = await store.user_accessor.create_user(
            session=nested_session.session,
            email=user_data.email,
            username=user_data.username,
            password=hashed_password,
        )

    return user
