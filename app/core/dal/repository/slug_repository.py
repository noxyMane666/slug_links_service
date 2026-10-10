from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dal.models.db_models import ShortURL


class SlugRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_slug(self, slug: str, long_url: str):
        new_slug = ShortURL(
            slug=slug,
            long_url=long_url
        )
        try:
            self._session.add(new_slug)
            await self._session.commit()
        except Exception:
            await self._session.rollback()
            raise


    async def get_long_url_by_slug(self, slug: str) -> str | None:
        query = select(ShortURL.long_url).where(
            ShortURL.slug == slug
        )

        return await self._session.scalar(query)
