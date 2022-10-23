from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends, Path
from starlette import status

from accessors.integration.users import get_user
from accessors.pot import get_pot_by
from orm.pot import pot_schema_out
from responses.okay import okay_response
from schemas.integration.user import UserSchema
from structures.enums import FilterEnum
from structures.named_tuples import attribute

view_router = APIRouter()


@view_router.get(path='.view/{user_id}',
                 status_code=status.HTTP_200_OK)
async def view_profile(user_id: int = Path(...)) -> dict:
    pot = await get_pot_by(attr=attribute(filter=FilterEnum.user_id), value=user_id)
    if pot is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'pot for user {user_id=} not found on server')
    pot_out = await pot_schema_out.from_tortoise_orm(pot)

    return okay_response(detail={
        'pot': pot_out.dict()
    })


@view_router.get(path='.me.view',
                 status_code=status.HTTP_200_OK)
async def view_me(user: UserSchema = Depends(get_user)) -> dict:
    return await view_profile(user_id=user.id)
