from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends, Query
from starlette import status

from accessors.integration.users import get_user, get_user_admin
from accessors.pot import create_pot, get_pot_by, update_pot
from orm.pot import pot_schema_in, pot_schema_out
from responses.okay import okay_response
from schemas.integration.user import UserSchema
from structures.enums import FilterEnum
from structures.named_tuples import attribute
from utils.decorators import admin_required

pot_router = APIRouter()


@pot_router.post(path='.me',
                 status_code=status.HTTP_201_CREATED)
async def me(user: UserSchema = Depends(get_user)) -> dict:
    pot = await create_pot(user_id=user.id)
    pot_out = await pot_schema_out.from_tortoise_orm(pot)

    return okay_response(detail={
        'pot': pot_out.dict()
    })


@pot_router.put(path='.update/{user_id}',
                status_code=status.HTTP_200_OK)
@admin_required(target='api_token')
async def update(data: pot_schema_in,
                 api_token: str = Query(...),
                 user: UserSchema = Depends(get_user_admin)) -> None:
    pot = await get_pot_by(attr=attribute(filter=FilterEnum.user_id), value=user.id)
    if pot is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'pot for user {user.id=} not found on server')
    await update_pot(pot=pot,
                     data=data.dict())

    return okay_response(detail={
        'message': 'updated'
    })
