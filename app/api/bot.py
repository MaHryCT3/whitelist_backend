from fastapi import APIRouter, BackgroundTasks, HTTPException, Request, Response, status
from loguru import logger

from app.config import settings
from app.services.vk_bot.bot import whitelist_bot

bot_router = APIRouter(prefix='/vk-bot')


@bot_router.post('/')
async def bot_handler(request: Request, background_task: BackgroundTasks) -> Response:
    data = await try_get_data(request)
    if is_confirmation(data):
        return Response(settings.CONFIRMATION_CODE)
    validate_secret_key(data)
    background_task.add_task(whitelist_bot.process_event, data)
    return Response('ok')


async def try_get_data(request: Request) -> dict:
    try:
        return await request.json()
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail='Body is invalid')


def is_confirmation(data: dict) -> bool:
    if data.get('type') == 'confirmation':
        return True
    return False


def validate_secret_key(data: dict) -> None:
    if data.get('secret') != settings.SECRET_KEY:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail='Secret key is invalid')
