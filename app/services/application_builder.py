from dataclasses import dataclass
from datetime import datetime

from loguru import logger

from app.db.tables.choices import ApprovalStatusChoices
from app.services.RCC.models import RCCBan
from app.services.RCC.service import RustCheatCheckService


@dataclass
class Application:
    telegram_username: str
    steamid: str
    bans: list[RCCBan] | None = None
    approve_status: ApprovalStatusChoices = ApprovalStatusChoices.AWAITING

    def to_string(self) -> str:
        text = f'Заявка от https://t.me/{self.telegram_username}\n'
        text += f'SteamID: {self.steamid}\n'
        text += f'Баны: {self.bans_text}\n'
        return text

    @property
    def bans_text(self) -> str:
        if self.bans is None:
            return 'Не удалось получить информацию о банах.'

        bans = ''
        for ban in self.bans:
            new_ban = f'{ban.server_name}: {ban.reason}. '
            if ban.is_active:
                start_ban = self._format_datetime(datetime.fromtimestamp(ban.ban_time))
                end_ban = (
                    self._format_datetime(datetime.fromtimestamp(ban.unban_time)) if ban.unban_time else 'Навсегда'
                )
                new_ban += f'Период бана: {start_ban} - {end_ban}'
                new_ban = '❌' + new_ban
            else:
                new_ban = '✅' + new_ban
            bans += f'\n{new_ban}'
        return bans

    def _format_datetime(self, dt: datetime) -> str:
        return dt.strftime('%d/%m/%Y')


class ApplicationBuilder:
    def __init__(self) -> None:
        self.rcc_service = RustCheatCheckService()

    async def build(self, telegram_username: str, steamid: str) -> Application:
        try:
            bans = await self._get_player_bans(steamid)
        except Exception as e:
            logger.exception(e)
            bans = None

        return Application(
            telegram_username=telegram_username,
            steamid=steamid,
            bans=bans,
        )

    async def _get_player_bans(self, steamid: str) -> list[RCCBan]:
        rcc_player = await self.rcc_service.get_player(steamid)
        return rcc_player.bans
