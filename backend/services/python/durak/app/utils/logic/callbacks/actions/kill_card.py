from accessors.card import get_card_by, is_on_table, update_card, get_table_cards
from structures.enums import FilterEnum, CardTypeEnum
from structures.named_tuples import attribute
from utils.decorators import game_started_required
from utils.logic.connection import Connection
from utils.logic.game import Game


@game_started_required
async def kill_card_callback(game: Game,
                             sender: Connection,
                             message: dict) -> None:
    card_id, to_be_killed_card_id = message.get('card_id'), message.get('kill_card_id')

    killed_card = await get_card_by(attr=attribute(filter=FilterEnum.id), value=to_be_killed_card_id)
    card = await get_card_by(attr=attribute(filter=FilterEnum.id), value=card_id)

    if (not card or card.player_id != sender.player.id or
            not killed_card or not is_on_table(card=killed_card)):
        return await game.personal_json(connection=sender,
                                        json={
                                            'ok': False,
                                            'message': 'card not found'
                                        })
    await update_card(card=card,
                      data={
                          'player_id': 0,
                          'card_type': CardTypeEnum.table.value,
                          'killed': True,
                          'killed_by': killed_card.id
                      })

    cards = await get_table_cards(game=sender.player.game)

    await game.broadcast_json(json={
        'type': 'kill_card',
        'table': cards
    })
