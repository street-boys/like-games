from typing import Any

from orm.chat import ChatModel
from orm.user import UserModel
from structures.enums import ChatTypeEnum
from structures.named_tuples import attribute


async def create_user(user_id: int) -> UserModel:
    user = await UserModel.get_or_create(id=user_id, user_id=user_id)

    return user[0]


async def get_user_by(attr: attribute, value: Any) -> UserModel:
    __filter = {attr.filter.name: value}

    user = await UserModel.get_or_none(**__filter)

    return user


async def can_get_chat(user: UserModel, chat: ChatModel) -> bool:
    if chat.chat_type == ChatTypeEnum.public:
        return True

    u = await chat.users.filter(id=user.id).first()

    return u is not None
