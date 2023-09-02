from vkbottle.bot import BotLabeler, Message
from vkbottle.tools.dev.uploader import DocMessagesUploader
from app.db.crud import UserCRUD

from app.db.session import SessionLocal

whitelist_labeler = BotLabeler()


@whitelist_labeler.message(text='/whitelist')
async def get_whitelist_steamids(message: Message) -> None:
    user_crud = UserCRUD()

    async with SessionLocal() as session:
        steamids = await user_crud.get_whitelist_steamids(session)

    if not steamids:
        return await message.answer('Вайтлист пуст')

    steamids_str = '\n'.join(steamids)
    steamids_bytes = steamids_str.encode('utf-8')

    uploader = DocMessagesUploader(message.ctx_api)

    whitelist_file = await uploader.upload('whitelist.txt', steamids_bytes, peer_id=message.peer_id)
    await message.answer(attachment=whitelist_file, dont_parse_links=True)


