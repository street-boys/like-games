from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends, Path
from fastapi.responses import Response
from starlette import status

from accessors.integration.users import get_user
from accessors.profile import get_profile_by
from orm.profile import profile_schema_out
from responses.okay import okay_response
from schemas.integration.user import UserSchema
from structures.enums import FilterEnum
from structures.named_tuples import attribute

view_router = APIRouter()


@view_router.get(path='.view/{user_id}',
                 status_code=status.HTTP_206_PARTIAL_CONTENT)
async def view_profile(user_id: int = Path(...)) -> dict:
    profile = await get_profile_by(attr=attribute(filter=FilterEnum.user_id), value=user_id)
    if profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'profile for user {user_id=} not found on server')
    profile_out = await profile_schema_out.from_tortoise_orm(profile)

    return okay_response(detail={
        'profile': profile_out.dict()
    })


@view_router.get(path='.view.image/{user_id}',
                 status_code=status.HTTP_206_PARTIAL_CONTENT)
async def view_profile_image(user_id: int = Path(...)) -> Response:
    profile = await get_profile_by(attr=attribute(filter=FilterEnum.user_id), value=user_id)
    if profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'profile for user {user_id=} not found on server')

    return Response(status_code=status.HTTP_206_PARTIAL_CONTENT,
                    content=profile.profile_image,
                    media_type=profile.profile_image_content_type)


@view_router.get(path='.me.view',
                 status_code=status.HTTP_206_PARTIAL_CONTENT)
async def view_me(user: UserSchema = Depends(get_user)) -> dict:
    return await view_profile(user_id=user.id)


@view_router.get(path='.me.view.image',
                 status_code=status.HTTP_206_PARTIAL_CONTENT)
async def view_me_image(user: UserSchema = Depends(get_user)) -> dict:
    return await view_profile_image(user_id=user.id)
