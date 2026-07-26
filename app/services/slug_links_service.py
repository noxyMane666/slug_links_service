from app.enums.app_enums import RequestStatus
from app.utlis.slug_generator import SlugGenerator
from app.dal.repository.slug_repository import SlugRepository
from app.models.models import SlugGenerationResult, RedirectLookupResult


class SlugLinksService:
    def __init__(self, sl_gen: SlugGenerator, slug_repo: SlugRepository):
        self.sl_gen = sl_gen
        self.repo = slug_repo

    async def generate_slug(self, long_url: str) -> SlugGenerationResult:
        slug = self.sl_gen.generate()
        #TODO обработка исключений
        await self.repo.add_slug_to_db(slug, long_url)
        return SlugGenerationResult(slug=slug, status=RequestStatus.Ok)

    async def get_long_url(self, slug: str) -> RedirectLookupResult:
        long_url = await self.repo.extract_long_url_from_db(slug)

        if not long_url:
            return RedirectLookupResult(status=RequestStatus.Error)

        return RedirectLookupResult(status=RequestStatus.Ok)


