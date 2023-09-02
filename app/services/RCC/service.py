from typing import Final

from app.config import settings
from app.services.http import HTTPClient
from app.services.RCC.models import RCCPlayer


class RustCheatCheckService(HTTPClient):
    BASE_URL: Final[str] = 'https://rustcheatcheck.ru/panel/api/'

    API_KEY: Final[str] = settings.RCC_KEY

    GET_PLAYER_ACTION: Final[str] = 'getInfo'

    async def get_player(self, steamid: str) -> RCCPlayer:
        response = await self.request('', 'GET', query=self._get_query(self.GET_PLAYER_ACTION, player=steamid))
        raw_player = await response.json()
        return RCCPlayer(**raw_player)

    def _get_query(self, action: str, **kwargs) -> dict:
        return {'action': action, 'key': self.API_KEY, **kwargs}
