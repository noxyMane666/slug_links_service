import pytest

from app.core.slug_generators.alph_slug_generator import AlphabetSlugGenerator


@pytest.mark.unit
def test_alph_slug_generation_len():
    slug = AlphabetSlugGenerator().generate()

    assert len(slug) == 6, "Length of slug can not be longer or shorter that 6 chars"