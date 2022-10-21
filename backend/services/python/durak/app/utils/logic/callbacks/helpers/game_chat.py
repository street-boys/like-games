from utils.logic.connection import Connection
from utils.logic.game import Game


async def kill_card_callback(game: Game,
                             sender: Connection,
                             message: dict) -> None:
    chat_id = game.game.chat_id

    if chat_id:
        await game.personal_json(connection=sender,
                                 json={
                                     'type': 'game_chat',
                                     'chat': {
                                         'id': chat_id
                                     }
                                 })
    else:
        await game.personal_json(connection=sender,
                                 json={
                                     'ok': False,
                                     'message': 'game not supported chat'
                                 })
