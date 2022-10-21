from typing import Any

from orm.chat import ChatModel
from orm.user import UserModel
from structures.enums import ChatTypeEnum
from structures.named_tuples import attribute


async def create_chat(chat_type: ChatTypeEnum = ChatTypeEnum.public) -> ChatModel:
    chat = await ChatModel.create(chat_type=chat_type)

    return chat


async def delete_chat(chat: ChatModel) -> None:
    await chat.delete()


async def get_user_chats(user: UserModel,
                         offset: int = 0,
                         limit: int = 0) -> list[ChatModel]:
    chats = await (ChatModel.filter(users__id=user.id).
                   offset(offset=offset).
                   limit(limit=limit))
    return chats


async def get_user_chats_count(user: UserModel) -> int:
    return await user.chats.all().count()


async def get_chat_by(attr: attribute, value: Any) -> ChatModel:
    __filter = {
        attr.filter.name: value
    }

    chat = await ChatModel.get_or_none(**__filter)

    return chat


async def get_users_in_chat(chat: ChatModel) -> list[UserModel]:
    return await chat.users.all()


async def is_users_in_the_same_chat(user_first: UserModel, user_second: UserModel) -> bool:
    async for chat_first in user_first.chats.all():
        if await user_second.chats.filter(id=chat_first.id):
            return True
    return False
