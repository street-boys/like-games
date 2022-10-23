from core.config import get_site_settings
from schemas.integration.chat import ChatSchema
from store import Store


async def create_game_chat(api_token: str,
                           store: Store) -> ChatSchema:
    base_url = get_site_settings().CHAT_SITE_BASE_URL
    async with store.aiohttp_accessor.session.post(url=f'{base_url}/api.chats.create.game',
                                                   params={
                                                       'api_token': api_token
                                                   },
                                                   raise_for_status=True) as response:
        json = await response.json()

    return ChatSchema(**json['detail']['chat'])
