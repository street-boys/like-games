from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from starlette import status

from accessors.integration.users import get_user_request
from accessors.message import get_message_by
from accessors.user import can_get_chat, get_user_by
from responses.okay import okay_response
from schemas.integration.user import UserSchema
from structures.enums import FilterEnum
from structures.named_tuples import attribute

message_router = APIRouter()


@message_router.get(
    path=".messages.get/{message_id}", status_code=status.HTTP_201_CREATED
)
async def get_message(
    message_id: int, user: UserSchema = Depends(get_user_request)
) -> dict:
    user = await get_user_by(attr=attribute(FilterEnum.user_id), value=user.id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found call the path api.chats.users.me first",
        )

    message = await get_message_by(
        attr=attribute(filter=FilterEnum.id), value=message_id
    )
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="message not found"
        )

    is_can_get_chat = await can_get_chat(chat=await message.chat, user=user)
    if not is_can_get_chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="message not found"
        )

    return okay_response(detail={"message": message})
