import logging

from app.configurations.app_settings import SlugGeneratingSettings
from app.core.models.slug_models import SlugUpdateModel
from app.core.slug_generators.interface import SlugGenerator
from app.core.dal.repository.slug_repository import SlugRepository
from app.exceptions.domain_exceptions import (
    SlugAlreadyExistsException,
    SlugIdentifierCollision
)
from app.api.models.dto import (
    GenerationSlugRequestDTO,
    BaseSlugResponseDTO
)

logger = logging.getLogger(__name__)


class SlugLinksService:
    def __init__(self, sl_gen: SlugGenerator, slug_repo: SlugRepository, config: SlugGeneratingSettings):
        self._sl_gen = sl_gen
        self._repo = slug_repo
        self._config = config

    async def generate_slug(self, long_url_dto: GenerationSlugRequestDTO) -> BaseSlugResponseDTO:
        attempts_count = 0
        slug = ""

        while attempts_count < self._config.generation_collision_overflow:
            slug = self._sl_gen.generate()
            try:
                slug_obj = await self._repo.add_slug(slug, str(long_url_dto.long_url))
                logger.info("Slug generated", extra={"event": "slug_generated", "slug": slug})
                return BaseSlugResponseDTO.model_validate(slug_obj)
            except SlugIdentifierCollision:
                logger.error("Slug generation failed", extra={
                    "event": "slug_generation_failed",
                    "slug": slug,
                    "attempt": attempts_count + 1
                })
            finally:
                attempts_count += 1

        raise SlugAlreadyExistsException(slug)


    async def get_long_url_to_redirect(self, slug: str) -> BaseSlugResponseDTO:
        slug_obj = await self._repo.get_slug(slug)
        slug_update_model = SlugUpdateModel(slug=slug, redirect_count=slug_obj.redirect_count + 1)
        await self._repo.update_slug(slug_update_model)

        logger.info("Slug resolved", extra={"event": "slug_resolved", "slug": slug})
        return BaseSlugResponseDTO.model_validate(slug_obj)

