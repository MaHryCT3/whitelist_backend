from vkbottle import GroupEventType
from vkbottle.bot import BotLabeler, Message, MessageEvent

from app.db.crud import UserCRUD
from app.db.session import SessionLocal
from app.db.tables.choices import ApprovalStatusChoices
from app.services.telegram import TelegramService
from app.services.vk_bot.payloads import ApproveApplicationPayload, DeclineApplicationPayload
from app.services.vk_bot.rules import PydanticPayloadRule

ERROR_TEXT_BEFORE_MESSAGE: str = 'Произошла ошибка.'
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
        user = await user_crud.update_approval_status(
            session, payload.approve_application_user_id, ApprovalStatusChoices.APPROVED
        )

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
        user = await user_crud.update_approval_status(
            session, payload.decline_application_user_id, ApprovalStatusChoices.DENIED
        )

    message_id = event.conversation_message_id
    await event.show_snackbar('Заявка отклонена')
    await event.ctx_api.messages.delete(delete_for_all=True, cmids=[message_id], peer_id=event.peer_id)
    await send_notification_to_telegram(user.telegram_id, DENIED_TEXT_MESSAGE)


@application_labeler.message(text='/approve <steamid>')
async def approve_application_by_telegram_id(message: Message, steamid: str):
    user_crud = UserCRUD()

    async with SessionLocal() as session:
        user = await user_crud.by_steamid(session, steamid)
        await user_crud.update_approval_status(session, user.id, ApprovalStatusChoices.APPROVED)

    await send_notification_to_telegram(user.telegram_id, f'{ERROR_TEXT_BEFORE_MESSAGE} {APPROVE_TEXT_MESSAGE}')
    await message.reply('Заявка одобрена')


@application_labeler.message(text='/denied <steamid>')
async def decline_application_by_telegram_id(message: Message, steamid: str):
    user_crud = UserCRUD()

    async with SessionLocal() as session:
        user = await user_crud.by_steamid(session, steamid)
        await user_crud.update_approval_status(session, user.id, ApprovalStatusChoices.DENIED)

    await send_notification_to_telegram(user.telegram_id, f'{ERROR_TEXT_BEFORE_MESSAGE} {DENIED_TEXT_MESSAGE}')
    await message.reply('Заявка отклонена')


async def send_notification_to_telegram(telegram_id: int, message: str):
    await TelegramService().send_message(telegram_id, message)
