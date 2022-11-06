import core
from schemas.integration.user import UserViewSchema


class UserAccessor:
    async def get_user_by_telegram(self, telegram: int) -> UserViewSchema:
        base_url = core.config.get_site_settings().AUTH_SITE_BASE_URL
        async with core.tools.store.aiohttp_accessor.session.get(
            url=f"{base_url}/api.user.view.by/telegram/{telegram}", raise_for_status=True
        ) as response:
            json = await response.json()

        return UserViewSchema(**json["detail"]["user"])
