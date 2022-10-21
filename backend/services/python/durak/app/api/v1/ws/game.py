from fastapi import APIRouter
from fastapi.param_functions import Depends
from fastapi.exceptions import HTTPException
from fastapi.websockets import WebSocket, WebSocketDisconnect
from websockets.exceptions import ConnectionClosedError
from starlette import status

from accessors.game import get_game_by
from accessors.integration.users import get_user_websocket
from accessors.user import get_user_by, get_player_by, create_player
from schemas.integration.user import UserSchema
from structures.enums import FilterEnum
from structures.named_tuples import attribute

ws_game_router = APIRouter()


@ws_game_router.websocket(path='.connect/{game_id}')
async def chat_endpoint(websocket: WebSocket,
                        game_id: int,
                        user: UserSchema = Depends(get_user_websocket)) -> None:
    game = await get_game_by(attr=attribute(FilterEnum.id), value=game_id)
    if not game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='chat not found')
    user = await get_user_by(attr=attribute(FilterEnum.user_id), value=user.id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='user not found')
    player = await get_player_by(attr=attribute(FilterEnum.user_id), value=user.id)
    if player:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='already in game')
    player = await create_player(user=user, game=game)

