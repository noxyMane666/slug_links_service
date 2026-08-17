from fastapi import Depends
from fastapi.responses import RedirectResponse

from app.dependencies import app_dependencies as dpcs
from app.core.services.slug_links_service import SlugLinksService
from app.core.models.dto import SlugGenerationResultDTO, GenerationSlugRequestDTO


def register_routes(app):
    @app.post("/generate_slug")
    async def generate(
            long_url: GenerationSlugRequestDTO,
            slug_service: SlugLinksService = Depends(dpcs.get_slug_service)
    ) -> SlugGenerationResultDTO:
        return await slug_service.generate_slug(long_url)

    @app.get("/{slug}")
    async def get_link(
            slug: str,
            slug_service: SlugLinksService = Depends(dpcs.get_slug_service)
    ):
        result = await slug_service.get_long_url(slug)
        return RedirectResponse(
            url=str(result.long_url),
            status_code=302
        )



