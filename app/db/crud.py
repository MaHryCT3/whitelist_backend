from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import BaseDeclarative
from app.db.tables import User
from app.db.tables.choices import ApprovalStatusChoices

ModelType = TypeVar('ModelType', bound=BaseDeclarative)


class CRUDBase(Generic[ModelType]):
    model: ModelType

    async def get(self, session: AsyncSession, id: int) -> ModelType | None:
        return await session.get(self.model, id)

    async def save(self, session: AsyncSession, instance: ModelType) -> ModelType:
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance

    async def remove(self, session: AsyncSession, instance: ModelType) -> None:
        await session.delete(instance)
        await session.commit()


class UserCRUD(CRUDBase[User]):
    model = User

    async def get_whitelist_steamids(self, session: AsyncSession) -> list[str]:
        statement = select(self.model).filter(self.model.approval_status == ApprovalStatusChoices.APPROVED)
        results = await session.execute(statement)
        return [result[0].steamid for result in results]

    async def by_steamid(self, session: AsyncSession, steamid: str) -> User | None:
        statement = select(self.model).filter(self.model.steamid == steamid)
        result = await session.execute(statement)
        result = result.first()
        return result[0] if result else None

    async def by_telegram_id(self, session: AsyncSession, telegram_id: int) -> User | None:
        statement = select(self.model).filter(self.model.telegram_id == telegram_id)
        result = await session.execute(statement)
        result = result.first()
        return result[0] if result else None

    async def update_approval_status(
        self, session: AsyncSession, id: int, approval_status: ApprovalStatusChoices
    ) -> User:
        instance = await self.get(session, id)
        instance.approval_status = approval_status
        return await self.save(session, instance)

    async def create(self, session: AsyncSession, telegram_id: int, steamid: str) -> User:
        user = self.model(id=None, telegram_id=telegram_id, steamid=steamid)
        return await self.save(session, user)

    async def get_for_alert_notifications(self, session: AsyncSession) -> list[int]:
        statement = select(self.model).filter(
            self.model.alert_notifications == True, self.model.approval_status == ApprovalStatusChoices.APPROVED
        )
        results = await session.execute(statement)
        return [result[0].telegram_id for result in results]
