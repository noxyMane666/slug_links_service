import logging

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dal.models.db_models import ShortURL

logger = logging.getLogger(__name__)


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
        except IntegrityError:
            await self._session.rollback()
            logger.info("Slug collision on insert, transaction rolled back", extra={"event": "slug_collision"})
            raise
        except Exception:
            await self._session.rollback()
            logger.error("Unexpected DB error on slug insert, transaction rolled back", exc_info=True)
            raise


    async def get_long_url_by_slug(self, slug: str) -> str | None:
        query = select(ShortURL.long_url).where(
            ShortURL.slug == slug
        )

        return await self._session.scalar(query)
