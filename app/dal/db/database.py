from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class AppDataBase:
    def __init__(self, connection_string: str):
        self.engine: AsyncEngine = create_async_engine(
            connection_string,
            echo=False,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    async def close(self):
        await self.engine.dispose()