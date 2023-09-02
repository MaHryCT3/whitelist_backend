from vkbottle import Bot, Token, Keyboard, Callback
from vkbottle.bot import BotLabeler

from loguru import logger

from app.config import settings
from app.services.application_builder import Application
from app.services.vk_bot.handlers import labelers
from app.services.vk_bot.payloads import ApproveApplicationPayload, DeclineApplicationPayload


class WhitelistBot(Bot):
    TOKEN: Token = settings.VK_TOKEN
    BOT_LABELERS: list[BotLabeler] = labelers

    ADMIN_CHAT_PEER_ID: int = settings.ADMIN_CHAT_PEER_ID

    def __init__(self) -> None:
        super().__init__(self.TOKEN)
        self._load_labelers()

    def _load_labelers(self) -> None:
        for labeler in self.BOT_LABELERS:
            self.labeler.load(labeler)

    async def send_application(self, application: Application, user_id: int):
        logger.info(f'Отправка заявки: {application.steamid}')
        await self.api.messages.send(
            peer_id=self.ADMIN_CHAT_PEER_ID,
            message=application.to_string(),
            keyboard=self._get_application_inline_keyboard(user_id),
            random_id=0,
        )

    def _get_application_inline_keyboard(self, user_id: int) -> str:
        approve_callback = Callback('Принять', ApproveApplicationPayload(approve_application_user_id=user_id).dict())
        decline_callback = Callback('Отклонить', DeclineApplicationPayload(decline_application_user_id=user_id).dict())

        keyboard = Keyboard(inline=True)
        keyboard.add(approve_callback)
        keyboard.add(decline_callback)
        return keyboard.get_json()


whitelist_bot = WhitelistBot()
