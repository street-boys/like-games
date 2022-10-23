from fastapi import APIRouter
from fastapi.datastructures import UploadFile
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends, File
from starlette import status

from accessors.integration.users import get_user
from accessors.profile import create_profile, get_profile_by, update_profile
from orm.profile import profile_schema_in, profile_schema_out
from responses.okay import okay_response
from schemas.integration.user import UserSchema
from structures.enums import FilterEnum, ProfileImageContentTypeEnum
from structures.named_tuples import attribute

profile_router = APIRouter()


@profile_router.post(path='.me',
                     status_code=status.HTTP_201_CREATED)
async def me(user: UserSchema = Depends(get_user)) -> dict:
    profile = await create_profile(user_id=user.id)
    profile_out = await profile_schema_out.from_tortoise_orm(profile)

    return okay_response(detail={
        'profile': profile_out.dict()
    })


@profile_router.put(path='.me.update.image',
                    status_code=status.HTTP_200_OK)
async def update_image(user: UserSchema = Depends(get_user),
                       image: UploadFile = File(default=None,
                                                media_type=ProfileImageContentTypeEnum)) -> dict:
    profile = await get_profile_by(attr=attribute(filter=FilterEnum.user_id), value=user.id)
    if profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'profile for user {user.id=} not found on server')
    await update_profile(profile=profile,
                         data={
                             'profile_image': await image.read(),
                             'profile_image_content_type': image.content_type
                         })

    return okay_response(detail={
        'message': 'updated'
    })


@profile_router.put(path='.me.update.bio',
                    status_code=status.HTTP_200_OK)
async def update_image(data: profile_schema_in,
                       user: UserSchema = Depends(get_user)) -> None:
    profile = await get_profile_by(attr=attribute(filter=FilterEnum.user_id), value=user.id)
    if profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'profile for user {user.id=} not found on server')
    await update_profile(profile=profile,
                         data=data.dict())

    return okay_response(detail={
        'message': 'updated'
    })
