from typing import Any

from orm.game import GameModel
from orm.user import UserModel, PlayerModel
from structures.named_tuples import attribute


async def create_user(user_id: int) -> UserModel:
    user = await UserModel.get_or_create(id=user_id, user_id=user_id)

    return user[0]


async def get_user_by(attr: attribute, value: Any) -> UserModel:
    __filter = {
        attr.filter.name: value
    }

    user = await UserModel.get_or_none(**__filter)

    return user


async def create_player(user: UserModel,
                        game: GameModel) -> PlayerModel:
    player = await PlayerModel.get_or_create(user=user, game=game)

    return player[0]


async def get_player_by(attr: attribute, value: Any) -> PlayerModel:
    __filter = {
        attr.filter.name: value
    }

    player = await PlayerModel.get_or_none(**__filter)

    return player
