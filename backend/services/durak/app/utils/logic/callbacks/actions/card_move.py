from accessors.card import get_player_cards, get_card_by, is_player_card, update_card
from structures.enums import FilterEnum, CardTypeEnum
from structures.named_tuples import attribute
from utils.decorators import game_started_required
from utils.logic.connection import Connection
from utils.logic.game import Game


@game_started_required
async def card_move_callback(game: Game,
                             sender: Connection,
                             message: dict) -> None:
    card_id = message.get('card_id')
    card = await get_card_by(attr=attribute(filter=FilterEnum.id), value=card_id)

    if (not card or not is_player_card(player_id=sender.player.id,
                                       card=card)):
        return await game.personal_json(connection=sender,
                                        json={
                                            'ok': False,
                                            'message': 'card not found'
                                        })

    await update_card(card=card,
                      data={
                          'player_id': 0,
                          'card_type': CardTypeEnum.table.value
                      })

    cards = await get_player_cards(player_id=sender.player.id)

    await game.personal_json(connection=sender,
                             json={
                                 'type': 'card_move',
                                 'hand': cards
                             })
