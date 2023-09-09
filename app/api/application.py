from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Response, status
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_session
from app.db.crud import UserCRUD
from app.services.application_builder import ApplicationBuilder
from app.services.vk_bot.bot import whitelist_bot

application_router = APIRouter(prefix='/application')


@application_router.post('/')
async def application_create(
    telegram_id: int,
    telegram_username: str,
    steamid: str,
    *,
    session: AsyncSession = Depends(get_session),
    background_task: BackgroundTasks,
) -> Response:
    logger.info(f'Новая заявка telegram_id: {telegram_id}, steamid: {steamid}')
    user_crud = UserCRUD()
    # Если пользователь уже есть, отменяем заявочку
    if await user_crud.by_telegram_id(session, telegram_id):
        logger.info(f'Пользователь уже отправлял заявку telegram_id: {telegram_id}, steamid: {steamid}')
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Пользователь уже отправлял заявку')

    application_builder = ApplicationBuilder()
    application = await application_builder.build(telegram_username=telegram_username, steamid=steamid)
    logger.info(f'Полученная заявка: {application.steamid}')

    new_user = await user_crud.create(session, steamid=steamid, telegram_id=telegram_id)
    logger.info(f'Создан новый пользователь: {new_user}')

    background_task.add_task(whitelist_bot.send_application, application, new_user.id)
    return Response(status_code=status.HTTP_201_CREATED)
