from accessors.message import create_message
from orm.chat import ChatModel
from utils.logic.connection import Connection


class Chat:
    connections: set[Connection] = set()

    def __init__(self, chat: ChatModel) -> None:
        self.chat = chat

    def __hash__(self) -> int:
        return self.chat.id

    @property
    def connections_length(self) -> int:
        return len(self.connections)

    async def add(self, connection: Connection) -> None:
        self.connections.add(connection)

    def remove(self, connection: Connection) -> None:
        self.connections.remove(connection)

    @staticmethod
    async def personal_json(connection: Connection, json: dict) -> None:
        await connection.websocket.send_json(json)

    @staticmethod
    async def personal_chat(connection: Connection, text: str) -> None:
        await connection.websocket.send_json(text)

    async def broadcast_json(self, text: dict) -> None:
        for connection in self.connections:
            await connection.websocket.send_json(text)


class ChatsManager:
    def __init__(self) -> None:
        self.chats = {}

    def add_chat(self, chat: Chat) -> None:
        if chat.chat.id not in self.chats:
            self.chats[chat.chat.id] = chat

    def remove_chat(self, chat: Chat) -> None:
        if not chat.connections_length:
            self.chats.pop(chat.chat.id)

    async def add_user(self, chat: Chat, connection: Connection) -> Chat:
        chat = self.chats[chat.chat.id]
        await chat.add(connection)
        return chat

    def remove_user(self, chat: Chat, connection: Connection) -> None:
        chat = self.chats[chat.chat.id]
        chat.remove(connection)
