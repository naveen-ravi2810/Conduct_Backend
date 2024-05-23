import redis.asyncio as redis
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.settings import settings

engine: AsyncEngine = create_async_engine(settings.DB_URI)


async_session = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncSession:  # type: ignore
    async with async_session() as session:
        yield session


# Connecting redis for auth_token and email_verification
r_conn = redis.Redis(
    host=settings.REDIS_HOST,
    db=settings.REDIS_DB,
    port=settings.REDIS_PORT,
)

# Connecction redis for ratelimiter purpose
r_conn_rate_limiter = redis.Redis(
    host=settings.REDIS_HOST,
    db=settings.REDIS_DB_RATE_LIMITER,
    port=settings.REDIS_PORT,
)
