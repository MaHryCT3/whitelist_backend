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


@whitelist_labeler.message(text='/remove <steamid>')
async def remove_steamid_from_whitelist(message: Message, steamid: str) -> None:
    user_crud = UserCRUD()

    async with SessionLocal() as session:
        user = await user_crud.by_steamid(session, steamid)

    if not user:
        return await message.answer('Пользователя с таким стиайди нету.')

    async with SessionLocal() as session:
        await user_crud.remove(session, user)

    await message.answer('Пользователь удален из вайтлиста.')
