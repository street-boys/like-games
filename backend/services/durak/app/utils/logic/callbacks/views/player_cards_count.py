from accessors.card import get_player_cards_count
from accessors.user import get_player_by
from structures.enums import FilterEnum
from structures.named_tuples import attribute
from utils.decorators import game_started_required
from utils.logic.connection import Connection
from utils.logic.game import Game


@game_started_required
async def player_cards_count_callback(game: Game,
                                      sender: Connection,
                                      message: dict) -> None:
    player_id = message.get('player_id')
    player = await get_player_by(attr=attribute(filter=FilterEnum.id), value=player_id)

    if not player or player.in_game_order == 0:
        return await game.personal_json(connection=sender,
                                        json={
                                            'ok': False,
                                            'message': 'player not in the game'
                                        })
    await game.personal_json(connection=sender,
                             json={
                                 'type': 'view_deck_count',
                                 'count': await get_player_cards_count(player_id=player.id)
                             })
