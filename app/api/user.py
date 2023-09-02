from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_session
from app.db.crud import UserCRUD

user_router = APIRouter(prefix='/user')


@user_router.get('/exist')
async def user_exist(telegram_id: int, *, session: AsyncSession = Depends(get_session)) -> Response:
    user_crud = UserCRUD()
    user = await user_crud.by_telegram_id(session, telegram_id)
    if user:
        return Response(status_code=status.HTTP_200_OK)
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@user_router.get('/steamid/exist')
async def steamid_exist(steamid: str, *, session: AsyncSession = Depends(get_session)) -> Response:
    user_crud = UserCRUD()
    user = await user_crud.by_steamid(session, steamid)
    if user:
        return Response(status_code=status.HTTP_200_OK)
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)