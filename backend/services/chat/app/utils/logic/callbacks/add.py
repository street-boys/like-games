from accessors.message import create_message
from orm.message import message_schema_out
from utils.logic.chat import Chat
from utils.logic.connection import Connection


async def add_callback(chat: Chat, sender: Connection, message: dict) -> None:
    text = message.get("data").get("text")

    if text:
        message = await create_message(
            chat=chat.chat, message_from=sender.user, text=text
        )
        message_out = await message_schema_out.from_tortoise_orm(message)

        await chat.broadcast_json({"type": "add", "message": message_out.dict()})
