from fastapi import Body

from app.models.models import SlugGenerationResult, RedirectLookupResult
from app.dependencies import app_dependencies as dpcs
from app.services.slug_links_service import SlugLinksService


def register_routes(app):
    @app.post("/generate_slug")
    async def generate(
            long_url: Body(embed=True),
            slug_service: SlugLinksService=dpcs.get_slug_service
    ) -> SlugGenerationResult:
        return await slug_service.generate_slug(long_url)

    @app.get("/{slug}")
    async def get_link(
            slug: Body(embed=True),
            slug_service: SlugLinksService=dpcs.get_slug_service
    ) -> RedirectLookupResult:
        return await slug_service.get_long_url(slug)



