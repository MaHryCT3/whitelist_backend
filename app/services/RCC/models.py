import time
from enum import Enum

from pydantic import BaseModel, Field, validator


class RCCErrorsMessages(Enum):
    INCORRECT_STEAMID: str = 'Неверный формат SteamID'
    NO_RCC_DATA: str = 'Игрок не вызывался на проверку и баны отсутствуют'
    KEY_NOT_FOUND: str = 'API ключ не найден'


class RCCResponseStatus(Enum):
    """RCC response status enum."""

    SUCCESS = 'success'
    ERROR = 'error'


class RCCBaseResponse(BaseModel):
    status: RCCResponseStatus
    error_message: RCCErrorsMessages | str = Field(None, alias='errorreason')


class RCCCheck(BaseModel):
    moder_steamid: int | None = Field(0, alias='moderSteamID')
    time: int
    server_name: str | None = Field(None, alias='serverName')


class RCCBan(BaseModel):
    ban_id: int | None = Field(None, alias='banID')
    reason: str
    server_name: str = Field('Без названия', alias='serverName')
    OVH_server_id: int = Field(None, alias='OVHserverID')
    ban_time: int = Field(0, alias='banDate')
    unban_time: int = Field(0, alias='unbanDate')
    active: bool

    @validator('ban_time', 'unban_time', 'OVH_server_id', pre=True)
    def validate_integers(cls, value: int | str) -> int:
        if isinstance(value, str) and not value.isdigit():
            return 0
        return value

    @property
    def is_active(self) -> bool:
        if not self.active:
            return False

        if self.unban_time == 0:
            return True

        if self.unban_time > time.time():
            return True

        return False


class RCCPlayer(RCCBaseResponse):
    steamid: str | None
    last_nick: str | None
    checks_count: int = Field(0, alias='rcc_checks')
    last_ip: list[str] = Field(default_factory=list)
    checks: list[RCCCheck] = Field(alias='last_check', default_factory=list)
    bans: list[RCCBan] = Field(default_factory=list)
    another_accs: list[int] = Field(default_factory=list)
    proofs: list[str] = Field(default_factory=list)
