from fastapi.websockets import WebSocket

from orm.user import PlayerModel


class Connection:
    def __init__(self,
                 websocket: WebSocket,
                 player: PlayerModel) -> None:
        self.websocket = websocket
        self.player = player

    def __hash__(self) -> int:
        return self.player.id
