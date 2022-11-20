from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core import depends, tools
from orm import UserModel
from schemas.user import UserViewSchema
from structures.enums import FilterPathEnum

router = APIRouter()


@router.get(
    path=".view.by/{filter}/{value}",
    response_description="Returns the user by filter",
    response_model=UserViewSchema,
    status_code=status.HTTP_200_OK,
)
async def view_user(
    filter: FilterPathEnum = Path(FilterPathEnum.id),
    value: int = Query(...),
    session: AsyncSession = Depends(depends.get_session),
) -> UserViewSchema:
    match filter:
        case filter.id:
            where = UserModel.id == value
        case filter.telegram:
            where = UserModel.telegram == value
        case _:
            where = None

    user = await tools.store.user_accessor.get_user_by(session=session, where=where)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"unable to find user by {filter=}, by {value=}",
        )

    return user
