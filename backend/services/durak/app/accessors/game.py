from typing import Any

from orm.game import GameModel
from orm.user import PlayerModel
from structures.named_tuples import attribute


async def create_game() -> GameModel:
    game = await GameModel.create()

    return game


async def get_game_by(attr: attribute, value: Any) -> GameModel:
    __filter = {
        attr.filter.name: value
    }

    game = await GameModel.get_or_none(**__filter)

    return game


async def update_game(game: GameModel, data: dict) -> None:
    await game.update_from_dict(data=data)
    await game.save()


async def get_next_player(game: GameModel) -> PlayerModel:
    players = await game.players.all().order_by('in_game_order')

    for index, player in enumerate(players, start=0):
        if player.id == game.player:
            try:
                return players[index + 1]
            except IndexError:
                return players[0]
