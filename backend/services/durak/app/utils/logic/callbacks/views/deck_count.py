from accessors.card import get_deck_cards_count
from utils.decorators import game_started_required
from utils.logic.connection import Connection
from utils.logic.game import Game


@game_started_required
async def deck_count_callback(game: Game,
                              sender: Connection,
                              message: dict) -> None:
    await game.personal_json(connection=sender,
                             json={
                                 'type': 'view_deck_count',
                                 'count': await get_deck_cards_count(deck=await game.game.deck)
                             })
