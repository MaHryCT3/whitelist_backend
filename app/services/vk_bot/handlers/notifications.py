import asyncio
from typing import Final

from loguru import logger
from vkbottle.bot import BotLabeler, Message

from app.db.crud import UserCRUD
from app.db.session import SessionLocal
from app.services.telegram import TelegramService

MESSAGES_PER_SECOND: Final[int] = 20


notifications_labeler = BotLabeler()


@notifications_labeler.message(text='/notify <notify_message>')
async def send_notification(message: Message, notify_message: str) -> None:
    async with SessionLocal() as session:
        users = await UserCRUD().get_for_alert_notifications(session)

    telegram = TelegramService()
    for i in range(0, len(users), MESSAGES_PER_SECOND):
        await asyncio.sleep(1)
        users_slice = users[i : i + MESSAGES_PER_SECOND]
        for user in users_slice:
            try:
                await telegram.send_message(user, notify_message)
            except Exception as e:
                logger.error(f'Error while sending notification to {user}: {e}')

    await message.reply('Уведомления отправлены.')
