from typing import Any

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Path, Query
from starlette import status

from accessors.user import get_user_by
from orm.user import user_schema_view_out
from responses.okay import okay_response
from structures.enums import FilterPathEnum
from structures.named_tuples import attribute

view_router = APIRouter()


@view_router.get(path='.view.by/{filter}/{value}',
                 status_code=status.HTTP_200_OK)
async def view_user(filter: FilterPathEnum = Path(FilterPathEnum.id),
                    value: Any = Query(...)):
    user = await get_user_by(attr=attribute(filter=filter), value=value)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'unable to find user by {filter=}, by {value=}')

    user_out = await user_schema_view_out.from_tortoise_orm(user)

    return okay_response(detail={
        'user': user_out.dict()
    })
