from typing import Any, Callable

from structures.enums import GameStateEnum
from utils.ws._answer import AnswerWSSchema


class game_in_wait_for_bet_required:
    def __init__(self,
                 function: Callable) -> None:
        self._function = function

    async def __call__(self, state: int, *args, **kwargs) -> Any:
        game = kwargs.get('game')

        if game.game.state == GameStateEnum.WAIT_FOR_BET.value:
            return await game.personal_json(connection=kwargs.get('sender'),
                                            json=AnswerWSSchema(ok=False,
                                                                type='undefined',
                                                                detail={'message': 'the game not started'}).dict())
        return await self._function(*args, **kwargs)
