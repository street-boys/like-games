from accessors.message import (
    get_messages_count_for_chat,
    get_messages_with_offset_and_limit,
)
from orm.message import messages_schema_out
from utils.logic.chat import Chat
from utils.logic.connection import Connection


async def view_callback(chat: Chat, sender: Connection, message: dict) -> None:
    offset, limit = (
        message.get("data").get("offset", 0),
        message.get("data").get("limit", 100),
    )
    count = await get_messages_count_for_chat(chat=chat.chat)

    messages = await get_messages_with_offset_and_limit(
        chat=chat.chat, offset=offset, limit=limit
    )
    messages_out = await messages_schema_out.from_queryset(messages)

    await chat.personal_json(
        connection=sender,
        json={
            "type": "view",
            "count": count,
            "messages": messages_out.dict().get("__root__"),
        },
    )
