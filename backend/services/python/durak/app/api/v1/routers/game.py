from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Query, Depends
from starlette import status

from accessors.game import create_game, get_game_by, update_game
from accessors.integration.chat import create_game_chat
from accessors.integration.users import get_user_request
from accessors.user import get_user_by, create_player, get_player_by
from core.depends import get_store
from responses.okay import okay_response
from schemas.integration.user import UserSchema
from store import Store
from structures.enums import FilterEnum
from structures.named_tuples import attribute
from utils.decorators import admin_required

game_router = APIRouter()


@game_router.post(path='.games.create')
@admin_required(target='api_token')
async def post_game(api_token: str = Query(...)) -> dict:
    game = await create_game()

    return okay_response(detail={
        'game': game
    })


@game_router.put(path='.games.add.chat/{game_id}')
@admin_required(target='api_token')
async def update_game_chat(api_token: str = Query(...),
                           game_id: int = Query(...),
                           store: Store = Depends(get_store)) -> dict:
    game = await get_game_by(attr=attribute(filter=FilterEnum.id), value=game_id)
    if not game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='game not found')
    if game.chat_id != 0:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='game chat already found')

    chat = await create_game_chat(api_token=api_token, store=store)

    await update_game(game=game,
                      data={
                          'chat_id': chat.id
                      })

    return okay_response(detail={
        'game': game
    })


@game_router.get(path='.games/{game_id}')
async def get_game(game_id: int = Query(...)) -> dict:
    game = await get_game_by(attr=attribute(filter=FilterEnum.user_id), value=game_id)
    if not game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='game not found')

    return okay_response(detail={
        'game': game
    })


@game_router.post(path='.games.join/{game_id}')
async def join(user: UserSchema = Depends(get_user_request),
               game_id: int = Query(...)) -> dict:
    player = await get_player_by(attr=attribute(filter=FilterEnum.user_id), value=user.id)

    return player
