from typing import Any

from tortoise.queryset import QuerySet

from orm.chat import ChatModel
from orm.message import MessageModel
from orm.user import UserModel
from structures.named_tuples import attribute


async def create_message(message_from: UserModel,
                         text: str,
                         chat: ChatModel) -> MessageModel:
    message = await MessageModel.create(text=text,
                                        message_from=message_from,
                                        chat=chat)

    return message


async def get_message_by(attr: attribute, value: Any) -> MessageModel:
    __filter = {
        attr.filter.name: value
    }

    message = await MessageModel.get_or_none(**__filter)

    return message


async def get_messages_count_for_chat(chat: ChatModel) -> int:
    count = await (MessageModel.filter(chat=chat).
                   count())

    return count


async def get_messages_with_offset_and_limit(chat: ChatModel,
                                             offset: int = 0,
                                             limit: int = 0) -> QuerySet[MessageModel]:
    messages = (MessageModel.filter(chat=chat).
                offset(offset=offset).
                limit(limit=limit))

    return messages
