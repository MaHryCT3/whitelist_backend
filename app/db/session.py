from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config import settings

engine = create_async_engine(settings.DATABASE_URI)


SessionLocal = async_sessionmaker(
    autoflush=False,
    expire_on_commit=False,
    bind=engine,
)
