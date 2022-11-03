from fastapi.requests import Request

import core.tools
from core.config import get_site_settings
from schemas.integration.user import UserSchema, UserViewSchema


class UserAccessor:
    async def get_user(self, request: Request) -> UserSchema:
        base_url = get_site_settings().AUTH_SITE_BASE_URL
        async with core.tools.store.aiohttp_accessor.session.get(
            url=f"{base_url}/api.user.cookie.current",
            cookies=request.cookies,
            raise_for_status=True,
        ) as response:
            json = await response.json()

        return UserSchema(**json["detail"]["user"])

    async def get_user_by_id(self, user_id: int) -> UserViewSchema:
        base_url = get_site_settings().AUTH_SITE_BASE_URL
        async with core.tools.store.aiohttp_accessor.session.get(
            url=f"{base_url}/api.user.view/id/{user_id}", raise_for_status=True
        ) as response:
            json = await response.json()

        return UserViewSchema(**json["detail"]["user"])
