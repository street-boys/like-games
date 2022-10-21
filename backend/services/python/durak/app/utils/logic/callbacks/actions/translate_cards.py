from accessors.card import get_card_by, update_card, get_table_cards
from accessors.game import get_next_player, update_game
from structures.enums import FilterEnum, CardTypeEnum
from structures.named_tuples import attribute
from utils.decorators import game_started_required
from utils.logic.connection import Connection
from utils.logic.game import Game


@game_started_required
async def kill_card_callback(game: Game,
                             sender: Connection,
                             message: dict) -> None:
    card_id = message.get('card_id')

    card = await get_card_by(attr=attribute(filter=FilterEnum.id), value=card_id)

    if not card or card.player_id != sender.player.id:
        return await game.personal_json(connection=sender,
                                        json={
                                            'ok': False,
                                            'message': 'card not found'
                                        })
    cards = await get_table_cards(game=sender.player.game)
    for table_card in cards:
        if card.killed or card.rank != table_card.rank:
            return await game.personal_json(connection=sender,
                                            json={
                                                'ok': False,
                                                'message': 'unprocessable'
                                            })
    next_player = await get_next_player(game=game.game)

    await update_game(game=game, data={
        'player': next_player.id
    })

    await update_card(card=card,
                      data={
                          'player_id': 0,
                          'card_type': CardTypeEnum.table.value
                      })

    cards = await get_table_cards(game=sender.player.game)

    await game.broadcast_json(json={
        'type': 'kill_card',
        'table': cards
    })
