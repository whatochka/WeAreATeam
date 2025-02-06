from typing import Any

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from database.config import DBConfig

POOL_SIZE = 20
MAX_POOL_OVERFLOW = 5
CONNECT_TIMEOUT = 5


sessionmaker_kwargs = {
    "autoflush": False,
    "future": True,
    "expire_on_commit": False,
}


async def create_sessionmaker(
    db_settings: DBConfig,
    **kwargs: Any,
) -> async_sessionmaker[AsyncSession]:
    engine = create_engine(db_settings)
    return async_sessionmaker(bind=engine, **{**sessionmaker_kwargs, **kwargs})


def create_engine(config: DBConfig) -> AsyncEngine:
    return create_async_engine(
        str(config.db_url),
        pool_size=POOL_SIZE,
        max_overflow=MAX_POOL_OVERFLOW,
        connect_args={"connect_timeout": CONNECT_TIMEOUT},
        pool_pre_ping=True,
    )
