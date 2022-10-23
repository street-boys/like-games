from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Query, Path
from starlette import status

from accessors.user import get_user_by, update_user
from responses.okay import okay_response
from structures.enums import FilterEnum
from structures.named_tuples import attribute
from utils.decorators.admin import admin_required

update_router = APIRouter()


@update_router.put(path='.update.online/{user_id}',
                   status_code=status.HTTP_200_OK)
@admin_required(target='api_token')
async def update_online(api_token: str = Query(...),
                        user_id: int = Path(...),
                        online: bool = Query(...)) -> None:
    user = await get_user_by(attr=attribute(FilterEnum.id), value=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='user not found')

    await update_user(user=user,
                      values={
                          'online': online
                      })

    return okay_response(detail={
        'message': 'updated'
    })
