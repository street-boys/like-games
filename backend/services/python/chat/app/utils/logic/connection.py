from fastapi.websockets import WebSocket

from orm.user import UserModel


class Connection:
    def __init__(self,
                 websocket: WebSocket,
                 user: UserModel) -> None:
        self.websocket = websocket
        self.user = user

    def __hash__(self) -> int:
        return self.user.id
