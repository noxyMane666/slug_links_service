from typing import cast
from unittest.mock import Mock

import pytest
from pydantic import HttpUrl

from app.api.models.dto import GenerationSlugRequestDTO
from app.configurations.app_settings import SlugGeneratingSettings
from app.core.dal.repository.slug_repository import SlugRepository
from app.core.services.slug_links_service import SlugLinksService
from app.core.slug_generators.alph_slug_generator import AlphabetSlugGenerator
from app.core.slug_generators.interface import SlugGenerator


@pytest.fixture
def slug_generator_config():
    return SlugGeneratingSettings(collision_overflow=3)

@pytest.fixture
def alph_slug_generator():
    return Mock(spec=AlphabetSlugGenerator)

@pytest.fixture
def slug_repository():
    return Mock(spec=SlugRepository)

@pytest.fixture
def slug_links_service(
    alph_slug_generator: Mock,
    slug_repository: Mock,
    slug_generator_config: SlugGeneratingSettings,
) -> SlugLinksService:
    return SlugLinksService(
        sl_gen=cast(SlugGenerator, alph_slug_generator),
        slug_repo=cast(SlugRepository, slug_repository),
        config=slug_generator_config,
    )

@pytest.fixture
def generate_slugs(slug_generator_config: SlugGeneratingSettings):
    return [
        f"slg_{i}"
        for i in range(slug_generator_config.collision_overflow)
    ]

@pytest.fixture
def generate_request_dto():
    return GenerationSlugRequestDTO(long_url=HttpUrl("https://example.com"))