from fastapi import APIRouter
from fastapi.param_functions import Depends
from fastapi_jwt_auth import AuthJWT
from starlette import status

from accessors.user import get_user_by
from orm.user import user_schema_in_login, user_schema_out
from responses.okay import okay_response
from structures.enums import FilterEnum
from structures.named_tuples import attribute
from utils.auth import authenticate_user
from utils.decorators import login_required

cookie_router = APIRouter()


@cookie_router.post(path='.cookie.login',
                    status_code=status.HTTP_200_OK)
async def login(user_data: user_schema_in_login, authorize: AuthJWT = Depends()) -> dict:
    user = await authenticate_user(email=user_data.email, password=user_data.password)

    access_token = authorize.create_access_token(subject=user.email)
    refresh_token = authorize.create_refresh_token(subject=user.email)

    authorize.set_access_cookies(access_token)
    authorize.set_refresh_cookies(refresh_token)

    return okay_response(detail='successfully login')


@cookie_router.delete(path='.cookie.logout',
                      status_code=status.HTTP_200_OK)
@login_required(target='authorize', attribute='jwt_required')
async def logout(authorize: AuthJWT = Depends()) -> dict:
    authorize.unset_jwt_cookies()

    return okay_response(detail='successfully logout')


@cookie_router.get(path='.cookie.current',
                   status_code=status.HTTP_200_OK)
@login_required(target='authorize', attribute='jwt_required')
async def current(authorize: AuthJWT = Depends()) -> dict:
    current_user = authorize.get_jwt_subject()
    user = await get_user_by(attr=attribute(filter=FilterEnum.email), value=current_user)

    user_out = await user_schema_out.from_tortoise_orm(user)

    return okay_response(detail={
        'user': user_out.dict()
    })
