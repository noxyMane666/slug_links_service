from fastapi import Depends
from fastapi.responses import RedirectResponse

from app.core.services.slug_links_service import SlugLinksService
from app.api.dependencies import api_deps
from app.api.models.dto import GenerationSlugRequestDTO, BaseSlugResponseDTO


def register_routes(app):
    @app.post("/generate_slug")
    async def generate(
            long_url: GenerationSlugRequestDTO,
            slug_service: SlugLinksService = Depends(api_deps.get_slug_service)
    ) -> BaseSlugResponseDTO:
        return await slug_service.generate_slug(long_url)

    @app.get("/slugs/{slug}")
    async def get_link(
            slug: str,
            slug_service: SlugLinksService = Depends(api_deps.get_slug_service)
    ) -> RedirectResponse:
        result = await slug_service.get_long_url_to_redirect(slug)
        return RedirectResponse(
            url=str(result.long_url),
            status_code=302
        )



