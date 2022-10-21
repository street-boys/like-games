from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends, Query
from starlette import status

from accessors.card import get_player_cards_count
from accessors.game import get_game_by
from accessors.integration.users import get_user_request
from accessors.user import create_user, get_user_by, create_player, get_player_by
from orm.user import user_schema_out
from responses.okay import okay_response
from schemas.integration.user import UserSchema
from structures.enums import FilterEnum
from structures.named_tuples import attribute

users_router = APIRouter()


@users_router.post(path='.users.me',
                   status_code=status.HTTP_201_CREATED)
async def me(user: UserSchema = Depends(get_user_request)) -> dict:
    user = await create_user(user_id=user.id)
    user_out = await user_schema_out.from_tortoise_orm(user)

    return okay_response(detail={
        'user': user_out.dict()
    })


@users_router.post(path='.users.somes',
                   status_code=status.HTTP_201_CREATED)
async def somes(user: UserSchema = Depends(get_user_request)) -> dict:
    data = {
        'type': 'view_players',
        'players': []
    }

    player = await get_player_by(attr=attribute(filter=FilterEnum.id), value=user.id)
    data.get('players', []).append({
        'user_id': player.user_id,
        'is_in_game': not player.in_game_order == 0
    })

    return data


@users_router.post(path='.users.me.join/{game_id}')
async def join(user: UserSchema = Depends(get_user_request),
               game_id: int = Query(...)) -> dict:
    user = await get_user_by(attr=attribute(filter=FilterEnum.user_id), value=user.id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='user not found')
    game = await get_game_by(attr=attribute(filter=FilterEnum.id), value=game_id)

    if not game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='game not found')

    player = await create_player(user=user, game=game)

    return okay_response(detail={
        'player': player
    })
