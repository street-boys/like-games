from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.depends import get_session
from core.tools import store
from orm.user import UserModel
from schemas.user import UserLoginSchema, UserSchema
from utils.auth import authenticate_user
from utils.decorators import login_required
from utils.token import (
    create_token_and_set_to_cookies,
    get_jwt_subject,
    refresh_and_set_access_token,
    unset_cookies_token,
)

cookie_router = APIRouter()


@cookie_router.post(
    path=".cookie.login",
    response_description="The user on successful login",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
)
async def login(
    user_data: UserLoginSchema,
    authorize: AuthJWT = Depends(),
    session: AsyncSession = Depends(get_session),
) -> UserSchema:
    user = await authenticate_user(
        session=session, email=user_data.email, password=user_data.password
    )

    create_token_and_set_to_cookies(authorize=authorize, subject=user.id)

    return user


@cookie_router.delete(
    path=".cookie.logout",
    response_model=UserSchema,
    response_description="A user who has logged out",
    status_code=status.HTTP_200_OK,
)
@login_required(target="authorize", attribute="jwt_required")
async def logout(
    authorize: AuthJWT = Depends(), session: AsyncSession = Depends(get_session)
) -> UserSchema:
    current_user = unset_cookies_token(authorize=authorize)

    user = await store.user_accessor.get_user_by(
        session=session, where=(UserModel.id == current_user)
    )

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

    unset_cookies_token(authorize=authorize)

    return user


@cookie_router.post(
    path=".cookie.refresh",
    response_description="The user",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
)
@login_required(target="authorize", attribute="jwt_refresh_token_required")
async def refresh(
    authorize: AuthJWT = Depends(), session: AsyncSession = Depends(get_session)
) -> UserSchema:
    current_user = refresh_and_set_access_token(authorize=authorize)

    user = await store.user_accessor.get_user_by(
        session=session, where=(UserModel.id == current_user)
    )

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

    return user


@cookie_router.get(
    path=".cookie.current",
    response_description="The current user who called this method",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
)
@login_required(target="authorize", attribute="jwt_required")
async def current(
    authorize: AuthJWT = Depends(), session: AsyncSession = Depends(get_session)
) -> UserSchema:
    current_user = get_jwt_subject(authorize=authorize)

    user = await store.user_accessor.get_user_by(
        session=session, where=(UserModel.id == current_user)
    )

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

    return user
