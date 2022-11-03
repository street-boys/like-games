from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.depends import get_session
from core.tools import store
from orm.user import UserModel
from responses.okay import okay_response
from schemas.user import UserSchema
from utils.auth import authenticate_user

oauth2_router = APIRouter()
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api.user.oauth2.login")


@oauth2_router.post(path=".oauth2.login", status_code=status.HTTP_200_OK)
async def login(
    authorize: AuthJWT = Depends(),
    oauth_form: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
) -> dict:
    user = await authenticate_user(
        session=session, email=oauth_form.username, password=oauth_form.password
    )

    access_token = authorize.create_access_token(subject=user.id)

    return okay_response(detail={"access_token": access_token, "token_type": "bearer"})


async def get_user(
    authorize: AuthJWT = Depends(),
    token: str = Depends(oauth2_schema),
    session: AsyncSession = Depends(get_session),
) -> UserSchema:
    authorize.jwt_required(token=token)

    current_user = authorize.get_jwt_subject()
    user = await store.user_accessor.get_user_by(
        session=session, where=(UserModel.id == current_user)
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )

    user_out = UserSchema.from_orm(user)
    return user_out


@oauth2_router.get(path=".oauth2.current", status_code=status.HTTP_200_OK)
async def current(current_user: UserSchema = Depends(get_user)) -> dict:
    return okay_response(detail={"user": current_user.dict()})