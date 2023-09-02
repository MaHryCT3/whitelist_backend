from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import SessionLocal


async def get_session() -> AsyncSession:
    try:
        session = SessionLocal()
        yield session
    finally:
        await session.close()
