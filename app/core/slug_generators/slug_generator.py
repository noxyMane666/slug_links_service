import string
from random import choice

from app.abstractions.interfaces import SlugGenerator


class AlphabetSlugGenerator(SlugGenerator):
    def __init__(self):
        self._alphabet: str = string.ascii_letters + string.digits

    def generate(self) -> str:
        slug = ""
        for _ in range(6):
            slug += choice(self._alphabet)

        return slug

