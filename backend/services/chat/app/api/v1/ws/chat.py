from fastapi import APIRouter
from fastapi.param_functions import Depends
from fastapi.exceptions import HTTPException
from fastapi.websockets import WebSocket, WebSocketDisconnect
from websockets.exceptions import ConnectionClosedError
from starlette import status

from accessors.chat import get_chat_by
from accessors.integration.users import get_user_websocket
from accessors.user import get_user_by, can_get_chat
from core.tools import chats_manager
from schemas.integration.user import UserSchema
from structures.enums import FilterEnum
from structures.named_tuples import attribute
from utils.logic.chat import Chat
from utils.logic.connection import Connection
from utils.logic.handlers import handle_message

ws_chat_router = APIRouter()


@ws_chat_router.websocket(path='.connect/{chat_id}')
async def chat_endpoint(websocket: WebSocket,
                        chat_id: int,
                        user: UserSchema = Depends(get_user_websocket)):
    chat = await get_chat_by(attr=attribute(FilterEnum.id), value=chat_id)
    if not chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='chat not found')
    user = await get_user_by(attr=attribute(FilterEnum.user_id), value=user.id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='user not found')

    is_can_get_chat = await can_get_chat(user=user, chat=chat)
    if not is_can_get_chat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='chat not found')

    connection = Connection(websocket=websocket,
                            user=user)
    chats_manager.add_chat(chat=Chat(chat=chat))
    room = await chats_manager.add_user(chat=Chat(chat=chat), connection=connection)

    try:
        await websocket.accept()

        while True:
            message = await websocket.receive_json()
            await handle_message(chat=room, sender=connection, message=message)
    except (WebSocketDisconnect, ConnectionClosedError):
        chats_manager.remove_user(chat=room, connection=connection)
        chats_manager.remove_chat(chat=room)
