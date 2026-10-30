from unittest.mock import call

import pytest

from app.core.models.slug_models import SlugModel
from app.exceptions.domain_exceptions import (
    SlugIdentifierCollision,
    SlugAlreadyExistsException
)


async def raise_collision_exc(slug: str, *_):
    raise SlugIdentifierCollision(slug)

@pytest.mark.unit
async def test_generate_slug_success(
        slug_links_service,
        alph_slug_generator,
        slug_repository,
        generate_request_dto,
        generate_slugs,
):
    slug = generate_slugs[0]
    expected_result = SlugModel(
        long_url=str(generate_request_dto.long_url),
        slug=slug,
        redirect_count=0
    )

    alph_slug_generator.generate.return_value = slug
    slug_repository.add_slug.return_value = expected_result
    result = await slug_links_service.generate_slug(generate_request_dto)

    assert result == expected_result

    alph_slug_generator.generate.assert_called_once()
    slug_repository.add_slug.assert_awaited_once_with(
        slug,
        str(generate_request_dto.long_url)
    )

@pytest.mark.unit
async def test_generate_slug_collision_resolve(
        slug_links_service,
        alph_slug_generator,
        slug_repository,
        generate_request_dto,
        generate_slugs,
):
    slugs = generate_slugs[:2]

    expected_result = SlugModel(
        long_url=str(generate_request_dto.long_url),
        slug=slugs[1],
        redirect_count=0
    )

    alph_slug_generator.generate.side_effect = [
        slugs[0],
        slugs[1]
    ]
    slug_repository.add_slug.side_effect = (
        SlugIdentifierCollision(slugs[0]),
        expected_result
    )

    result = await slug_links_service.generate_slug(generate_request_dto)

    assert result == expected_result
    assert alph_slug_generator.generate.call_count == 2
    assert slug_repository.add_slug.await_count == 2

    slug_repository.add_slug.assert_has_awaits([
        call(slug, str(generate_request_dto.long_url))
        for slug in slugs
    ])

@pytest.mark.unit
async def test_generate_slug_collision_fail(
        slug_links_service,
        alph_slug_generator,
        slug_repository,
        generate_request_dto,
        generate_slugs,
):
    slugs = generate_slugs

    alph_slug_generator.generate.side_effect = slugs
    slug_repository.add_slug.side_effect = raise_collision_exc

    with pytest.raises(SlugAlreadyExistsException):
        await slug_links_service.generate_slug(generate_request_dto)

    assert alph_slug_generator.generate.call_count == 3
    assert slug_repository.add_slug.await_count == 3

    slug_repository.add_slug.assert_has_awaits([
        call(slug, str(generate_request_dto.long_url))
        for slug in slugs
    ])




