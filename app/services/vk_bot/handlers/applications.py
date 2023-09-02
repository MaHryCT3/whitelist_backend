from vkbottle import GroupEventType
from vkbottle.bot import BotLabeler, MessageEvent
from app.db.crud import UserCRUD

from app.services.vk_bot.rules import PydanticPayloadRule
from app.services.vk_bot.payloads import ApproveApplicationPayload, DeclineApplicationPayload
from app.db.tables.choices import ApprovalStatusChoices
from app.db.session import SessionLocal
from app.services.telegram import TelegramService


APPROVE_TEXT_MESSAGE: str = 'Поздравляю, Ваша заявка была одобрена!'
DENIED_TEXT_MESSAGE: str = 'К сожалению, Ваша заявка была отклонена.'

application_labeler = BotLabeler()


@application_labeler.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    PydanticPayloadRule(ApproveApplicationPayload),
)
async def approve_application(event: MessageEvent, payload: ApproveApplicationPayload):
    user_crud = UserCRUD()

    async with SessionLocal() as session:
        user = await user_crud.update_approval_status(session, payload.approve_application_user_id, ApprovalStatusChoices.SUCCESS)

    message_id = event.conversation_message_id
    await event.show_snackbar('Заявка одобрена')
    await event.ctx_api.messages.delete(delete_for_all=True, cmids=[message_id], peer_id=event.peer_id)
    await send_notification_to_telegram(user.telegram_id, APPROVE_TEXT_MESSAGE)


@application_labeler.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    PydanticPayloadRule(DeclineApplicationPayload),
)
async def decline_application(event: MessageEvent, payload: DeclineApplicationPayload):
    user_crud = UserCRUD()

    async with SessionLocal() as session:
        user = await user_crud.update_approval_status(session, payload.decline_application_user_id, ApprovalStatusChoices.DENIED)

    message_id = event.conversation_message_id
    await event.show_snackbar('Заявка отклонена')
    await event.ctx_api.messages.delete(delete_for_all=True, cmids=[message_id], peer_id=event.peer_id)
    await send_notification_to_telegram(user.telegram_id, DENIED_TEXT_MESSAGE)


async def send_notification_to_telegram(telegram_id: int, message: str):
    await TelegramService().send_message(telegram_id, message)
