from utils.logic.connection import Connection
from utils.logic.game import Game

from structures.enums import GameStateEnum
from utils.decorators import game_in_wait_for_bet_required
from utils.ws._answer import AnswerWSSchema


@game_in_wait_for_bet_required
async def raise_button_handler(game: Game,
                               sender: Connection,
                               message: dict) -> None:
    ...
