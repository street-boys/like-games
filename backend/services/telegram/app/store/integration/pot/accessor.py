import core
from schemas.integration.pot import PotSchema


class PotAccessor:
    async def get_user_pot(self, user_id: int) -> PotSchema:
        base_url = core.config.get_site_settings().POT_SITE_BASE_URL
        async with core.tools.store.aiohttp_accessor.session.get(
            url=f"{base_url}/api.pot.view/{user_id}", raise_for_status=True
        ) as response:
            json = await response.json()

        return PotSchema(**json["detail"]["pot"])
