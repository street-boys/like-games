from fastapi.param_functions import Depends
from fastapi.requests import Request
from fastapi.websockets import WebSocket

from core.config import get_site_settings
from core.depends import get_store
from schemas.integration.user import UserSchema
from store import Store


async def get_user_request(request: Request,
                           store: Store = Depends(get_store)) -> UserSchema:
    base_url = get_site_settings().AUTH_SITE_BASE_URL
    async with store.aiohttp_accessor.session.get(url=f'{base_url}/api.users.cookie.current',
                                                  cookies=request.cookies,
                                                  raise_for_status=True) as response:
        json = await response.json()

    return UserSchema(**json['detail']['user'])


async def get_user_websocket(websocket: WebSocket,
                             store: Store = Depends(get_store)) -> UserSchema:
    base_url = get_site_settings().AUTH_SITE_BASE_URL
    async with store.aiohttp_accessor.session.get(url=f'{base_url}/api.users.cookie.current',
                                                  cookies=websocket.cookies,
                                                  raise_for_status=True) as response:
        json = await response.json()

    return UserSchema(**json['detail']['user'])


async def update_online(store: Store,
                        user_id: int,
                        online: bool = False) -> dict:
    base_url = get_site_settings().AUTH_SITE_BASE_URL
    async with store.aiohttp_accessor.session.put(url=f'{base_url}/api.users.update.online/{user_id}',
                                                  raise_for_status=True) as response:
        json = await response.json()

    return json
