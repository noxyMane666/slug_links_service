from sqlalchemy.exc import IntegrityError

from app.abstractions.interfaces import SlugGenerator
from app.core.dal.repository.slug_repository import SlugRepository
from app.exceptions.domain_exceptions import LongUrlNotFoundException, SlugAlreadyExistsException
from app.core.models.dto import (
    SlugGenerationResultDTO,
    RedirectLookupResultDTO,
    GenerationSlugRequestDTO
)


class SlugLinksService:
    def __init__(self, sl_gen: SlugGenerator, slug_repo: SlugRepository):
        self.sl_gen = sl_gen
        self.repo = slug_repo

    async def generate_slug(self, long_url_dto: GenerationSlugRequestDTO) -> SlugGenerationResultDTO:
        slug = self.sl_gen.generate()
        try:
            await self.repo.add_slug_to_db(slug, str(long_url_dto.long_url))
            return SlugGenerationResultDTO(slug=slug)
        except IntegrityError:
            raise SlugAlreadyExistsException(slug)


    async def get_long_url(self, slug: str) -> RedirectLookupResultDTO:
        long_url = await self.repo.extract_long_url_from_db(slug)

        if not long_url:
            raise LongUrlNotFoundException(slug)

        return RedirectLookupResultDTO(long_url=long_url)

