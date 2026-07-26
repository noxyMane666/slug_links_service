from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dal.db.db_models import ShortURL


class SlugRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_slug_to_db(self, slug: str, long_url: str):
        #TODO обработка ошибок добавления
        new_slug = ShortURL(
            slug=slug,
            long_url=long_url
        )
        self._session.add(new_slug)
        await self._session.commit()

    async def extract_long_url_from_db(self, slug: str) -> str | None:
        query = select(ShortURL).where(
            ShortURL.slug == slug
        )

        result = await self._session.execute(query)
        short_url = result.scalar_one_or_none()

        if short_url is None:
            return None

        return short_url.long_url