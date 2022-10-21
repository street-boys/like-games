from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends, Query
from starlette import status

from accessors.chat import get_user_chats, get_user_chats_count
from accessors.integration.users import get_user_request
from accessors.user import create_user, get_user_by
from orm.user import user_schema_out
from responses.okay import okay_response
from schemas.integration.user import UserSchema
from structures.enums import FilterEnum
from structures.named_tuples import attribute

users_router = APIRouter()


@users_router.post(path='.users.me',
                   status_code=status.HTTP_201_CREATED)
async def me(user: UserSchema = Depends(get_user_request)) -> dict:
    user = await create_user(user_id=user.id)
    user_out = await user_schema_out.from_tortoise_orm(user)

    return okay_response(detail={
        'user': user_out.dict()
    })


@users_router.get(path='.users.me.chats',
                  status_code=status.HTTP_201_CREATED)
async def me_chats(user: UserSchema = Depends(get_user_request),
                   offset: int = Query(default=0),
                   limit: int = Query(default=100, le=100)) -> dict:
    user = await get_user_by(attr=attribute(FilterEnum.user_id), value=user.id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='user not found call the path api.chats.users.me first')

    user_chats_count = await get_user_chats_count(user=user)
    user_chats = await get_user_chats(user=user, offset=offset, limit=limit)

    return okay_response(detail={
        'count': user_chats_count,
        'chats': [{
            'id': chat.id,
            'type': chat.chat_type.value,
            'users': await chat.users.all()
        } for chat in user_chats]
    })
