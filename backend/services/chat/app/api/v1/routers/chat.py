from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends, Query
from starlette import status

from accessors.chat import (
    create_chat,
    delete_chat,
    get_chat_by,
    is_users_in_the_same_chat,
)
from accessors.integration.users import get_user_request
from accessors.user import can_get_chat, get_user_by
from responses.okay import okay_response
from schemas.integration.user import UserSchema
from structures.enums import ChatTypeEnum, FilterEnum
from structures.named_tuples import attribute
from utils.decorators.admin import admin_required

chat_router = APIRouter()


@chat_router.post(path=".create.game", status_code=status.HTTP_201_CREATED)
@admin_required(target="api_token")
async def create_game_chat(api_token: str = Query(...)) -> dict:
    chat = await create_chat(chat_type=ChatTypeEnum.public)

    return okay_response(detail={"chat": chat})


@chat_router.delete(path=".delete.game", status_code=status.HTTP_200_OK)
@admin_required(target="api_token")
async def delete_game_chat(
    api_token: str = Query(...), chat_id: int = Query(...)
) -> dict:
    chat = await get_chat_by(attr=attribute(FilterEnum.id), value=chat_id)
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="the game chat not found"
        )
    await delete_chat(chat=chat)

    return okay_response(detail="successfully deleted the game chat")


@chat_router.post(path=".create.private", status_code=status.HTTP_201_CREATED)
async def create_private_chat(
    user_first_depends: UserSchema = Depends(get_user_request),
    user_second_id: int = Query(...),
) -> dict:
    user_first = await get_user_by(
        attr=attribute(FilterEnum.user_id), value=user_first_depends.id
    )
    user_second = await get_user_by(
        attr=attribute(FilterEnum.user_id), value=user_second_id
    )

    if not user_first or not user_second:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="cannot find user"
        )

    if user_first.id == user_second.id:
        raise HTTPException(
            status_code=status.HTTP_418_IM_A_TEAPOT, detail="currently not supported"
        )
    if await is_users_in_the_same_chat(user_first, user_second):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="there is already a chat between users",
        )

    chat = await create_chat(chat_type=ChatTypeEnum.private)
    await chat.users.add(user_first, user_second)

    return okay_response(detail={"chat": chat})


@chat_router.delete(path=".delete.private", status_code=status.HTTP_200_OK)
async def delete_private_chat(
    user: UserSchema = Depends(get_user_request), chat_id: int = Query(...)
) -> dict:
    chat = await get_chat_by(attr=attribute(FilterEnum.id), value=chat_id)
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="chat not found"
        )
    user = await get_user_by(attr=attribute(FilterEnum.user_id), value=user.id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found "
        )
    is_can_get_chat = await can_get_chat(user=user, chat=chat)
    if not is_can_get_chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="chat not found"
        )
    await delete_chat(chat=chat)

    return okay_response(detail="successfully deleted chat")
