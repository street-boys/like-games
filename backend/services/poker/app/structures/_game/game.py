from utils.logic.connection import Connection

from orm.game import GameModel


class Game:
    connections: set[Connection] = set()

    def __init__(self, game: GameModel) -> None:
        self.game = game

    def __hash__(self) -> int:
        return self.game.id

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

    async def broadcast_json(self, json: dict) -> None:
        for connection in self.connections:
            await connection.websocket.send_json(json)
