import logging

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dal.models.db_models import ShortURL
from app.core.models.slug_models import SlugUpdateModel, SlugModel
from app.exceptions.domain_exceptions import LongUrlNotFoundException

logger = logging.getLogger(__name__)


class SlugRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_slug(self, slug: str, long_url: str) -> SlugModel:
        # TODO: Сделать redirect_count server_default = 0 и not nullable
        new_slug = ShortURL(
            slug=slug,
            long_url=long_url,
            redirect_count=0
        )
        try:
            self._session.add(new_slug)
            await self._session.commit()
            return SlugModel.model_validate(new_slug)
        except IntegrityError:
            await self._session.rollback()
            logger.info("Slug collision on insert, transaction rolled back", extra={"event": "slug_collision"})
            raise
        except Exception:
            await self._session.rollback()
            logger.error("Unexpected DB error on slug insert, transaction rolled back", exc_info=True)
            raise


    async def get_slug(self, slug: str) -> SlugModel:
        query = (
            select(ShortURL)
            .where(
                ShortURL.slug == slug
            )
        )

        try:
            slug_obj = await self._session.scalar(query)

            if not slug_obj:
                raise LongUrlNotFoundException(slug)

            return SlugModel.model_validate(slug_obj)
        except Exception:
            await self._session.rollback()
            logger.error("Unexpected DB error on slug update, transaction rolled back", exc_info=True)
            raise

    async def update_slug(self, update_model: SlugUpdateModel) -> SlugUpdateModel:
        query = (
            select(ShortURL)
            .where(
                ShortURL.slug == update_model.slug
            )
            .with_for_update()
        )

        try:
            slug_obj = await self._session.scalar(query)

            if not slug_obj:
                raise LongUrlNotFoundException(update_model.slug)

            update_data = update_model.model_dump(
                exclude_unset=True,
                exclude={"slug"}
            )

            for field, value in update_data.items():
                setattr(slug_obj, field, value)

            self._session.add(slug_obj)
            await self._session.commit()
            logger.info("Slug successfully updated", extra={"event": "slug_updating"})
            return  update_model
        except Exception:
            await self._session.rollback()
            logger.error("Unexpected DB error on slug update, transaction rolled back", exc_info=True)
            raise