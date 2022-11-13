from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from fastapi.requests import Request
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.depends import get_session
from core.tools import store
from orm.user import UserModel
from schemas.user import UserSchema
from utils.telegram import verify_telegram_authentication

telegram_router = APIRouter()


@telegram_router.post(
    path=".telegram.login",
    response_description="The user on successful login",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
)
async def login(
    request: Request, authorize: AuthJWT = Depends(), session: AsyncSession = Depends(get_session)
) -> UserSchema:
    try:
        request_data = verify_telegram_authentication(query=request.query_params)
    except TypeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="can't verify data")
    user = await store.user_accessor.get_user_by(
        session=session, where=(UserModel.telegram == request_data.id)
    )
    if not user:
        async with session.begin_nested() as nested_session:
            user = await store.user_accessor.create_user_telegram(
                session=nested_session.session,
                telegram=request_data.id,
                username=request_data.username,
            )

    access_token = authorize.create_access_token(subject=user.id)
    refresh_token = authorize.create_refresh_token(subject=user.id)

    authorize.set_access_cookies(access_token)
    authorize.set_refresh_cookies(refresh_token)

    return user
