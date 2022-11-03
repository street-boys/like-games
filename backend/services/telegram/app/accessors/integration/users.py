from core.config import get_site_settings
from core.tools import store
from schemas.integration.user import UserSchema


async def get_user_telegram(telegram: int) -> UserSchema:
    base_url = get_site_settings().AUTH_SITE_BASE_URL
    async with store.aiohttp_accessor.session.get(url=f'{base_url}/api.user.view.by/telegram/{telegram}',
                                                  raise_for_status=True) as response:
        json = await response.json()

    return UserSchema(**json['detail']['user'])
