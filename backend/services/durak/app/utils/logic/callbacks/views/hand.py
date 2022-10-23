from accessors.card import get_player_cards
from utils.decorators import game_started_required
from utils.logic.connection import Connection
from utils.logic.game import Game


@game_started_required
async def hand_callback(game: Game,
                        sender: Connection,
                        message: dict) -> None:
    cards = await get_player_cards(player_id=sender.player.id)
    await game.personal_json(connection=sender,
                             json={
                                 'type': 'view_hand',
                                 'hand': cards
                             })
