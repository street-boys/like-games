from accessors.card import get_table_cards
from utils.decorators import game_started_required
from utils.logic.connection import Connection
from utils.logic.game import Game


@game_started_required
async def table_callback(game: Game,
                         sender: Connection,
                         message: dict) -> None:
    cards = await get_table_cards(game=sender.player.game)

    await game.personal_json(connection=sender,
                             json={
                                 'type': 'view_hand',
                                 'table': cards
                             })
