from sqlalchemy.sql.expression import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.configurations.app_settings import DBSettings


class AppDataBase:
    def __init__(self, settings: DBSettings):
        self.engine: AsyncEngine = create_async_engine(
            str(settings.connection_string),
            echo=False,
            pool_size=settings.pool_size,
            max_overflow=settings.pool_max_overflow,
            pool_timeout=settings.pool_timeout
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    async def check_db_connection(self) -> None:
        async with self.engine.connect() as conn:
            await conn.execute(text("SELECT 1"))

    async def close(self):
        await self.engine.dispose()