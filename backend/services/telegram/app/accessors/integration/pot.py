from core.config import get_site_settings
from core.tools import store
from schemas.integration.pot import PotSchema


async def get_user_pot(user_id: int) -> PotSchema:
    base_url = get_site_settings().POT_SITE_BASE_URL
    async with store.aiohttp_accessor.session.get(url=f'{base_url}/api.pot.view/{user_id}',
                                                  raise_for_status=True) as response:
        json = await response.json()

    return PotSchema(**json['detail']['pot'])
