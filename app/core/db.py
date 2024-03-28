import redis.asyncio as redis
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import AsyncEngine

from app.core.settings import settings

engine: AsyncEngine = create_async_engine(settings.DB_URI)


async_session = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncSession:  # type: ignore
    async with async_session() as session:
        yield session


r_conn = redis.Redis(
    host=settings.REDIS_HOST, db=settings.REDIS_DB, port=settings.REDIS_PORT
)

# r = await redis.from_url("redis://localhost")
