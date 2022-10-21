from utils.decorators import game_started_required
from utils.logic.connection import Connection
from utils.logic.game import Game


@game_started_required
async def players_callback(game: Game,
                           sender: Connection,
                           message: dict) -> None:
    data = {
        'type': 'view_players',
        'players': []
    }

    for connection in game.connections:
        data.get('players', []).append({
            'user_id': connection.player.user_id,
            'is_in_game': not connection.player.in_game_order == 0
        })

    await game.personal_json(connection=sender,
                             json=data)
