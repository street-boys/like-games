from typing import Callable, Any

from structures.enums import GameStateEnum


class game_started_required:
    def __init__(self, function: Callable) -> None:
        self.function = function

    async def __call__(self, *args, **kwargs) -> Any:
        game = kwargs.get('game')

        if game.game.state == GameStateEnum.WAIT_FOR_PLAYERS:
            game.personal_json(connection=kwargs.get('sender'),
                               json={
                                   'ok': False,
                                   'message': 'the game not started'
                               })
        else:
            return await self.function(*args, **kwargs)


class game_in_ready_state_required:
    def __init__(self, function: Callable) -> None:
        self.function = function

    async def __call__(self, *args, **kwargs) -> Any:
        game = kwargs.get('game')

        if game.game.state == GameStateEnum.WAIT_FOR_READY:
            game.personal_json(connection=kwargs.get('sender'),
                               json={
                                   'ok': False,
                                   'message': 'game not in a ready state'
                               })
        else:
            return await self.function(*args, **kwargs)
