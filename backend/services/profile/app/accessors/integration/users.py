from fastapi.param_functions import Depends
from fastapi.requests import Request

from core.config import get_site_settings
from core.depends import get_store
from schemas.integration.user import UserSchema
from store import Store


async def get_user(request: Request,
                   store: Store = Depends(get_store)) -> UserSchema:
    base_url = get_site_settings().AUTH_SITE_BASE_URL
    async with store.aiohttp_accessor.session.get(url=f'{base_url}/api.user.cookie.current',
                                                  cookies=request.cookies,
                                                  raise_for_status=True) as response:
        json = await response.json()

    return UserSchema(**json['detail']['user'])
