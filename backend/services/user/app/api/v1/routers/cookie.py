from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.depends import get_session
from core.tools import store
from orm.user import UserModel
from responses.okay import okay_response
from schemas.user import UserLoginSchema, UserSchema
from utils.auth import authenticate_user
from utils.decorators import login_required

cookie_router = APIRouter()


@cookie_router.post(path=".cookie.login", status_code=status.HTTP_200_OK)
async def login(
    user_data: UserLoginSchema,
    authorize: AuthJWT = Depends(),
    session: AsyncSession = Depends(get_session),
) -> dict:
    user = await authenticate_user(
        session=session, email=user_data.email, password=user_data.password
    )

    access_token = authorize.create_access_token(subject=user.id)
    refresh_token = authorize.create_refresh_token(subject=user.id)

    authorize.set_access_cookies(access_token)
    authorize.set_refresh_cookies(refresh_token)

    return okay_response(detail="successfully login")


@cookie_router.delete(path=".cookie.logout", status_code=status.HTTP_200_OK)
@login_required(target="authorize", attribute="jwt_required")
async def logout(authorize: AuthJWT = Depends()) -> dict:
    authorize.unset_jwt_cookies()

    return okay_response(detail="successfully logout")


@cookie_router.post(".cookie.refresh")
@login_required(target="authorize", attribute="jwt_refresh_token_required")
def refresh(authorize: AuthJWT = Depends()) -> dict:
    current_user = authorize.get_jwt_subject()
    _ = authorize.create_access_token(subject=current_user)

    return okay_response(detail="token was updated")


@cookie_router.get(path=".cookie.current", status_code=status.HTTP_200_OK)
@login_required(target="authorize", attribute="jwt_required")
async def current(
    authorize: AuthJWT = Depends(), session: AsyncSession = Depends(get_session)
) -> dict:
    current_user = authorize.get_jwt_subject()

    user = await store.user_accessor.get_user_by(
        session=session, where=(UserModel.id == current_user)
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )

    user_out = UserSchema.from_orm(user)

    return okay_response(detail={"user": user_out.dict()})
