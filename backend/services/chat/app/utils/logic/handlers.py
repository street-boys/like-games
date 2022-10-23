from structures.enums import MessageTypeEnum
from utils.logic.callbacks.add import add_callback
from utils.logic.callbacks.view import view_callback
from utils.logic.chat import Chat
from utils.logic.connection import Connection


async def handle_message(chat: Chat,
                         sender: Connection,
                         message: dict) -> None:
    match message.get('type'):
        case MessageTypeEnum.view:
            await view_callback(chat=chat, sender=sender, message=message)

        case MessageTypeEnum.add:
            await add_callback(chat=chat, sender=sender, message=message)
