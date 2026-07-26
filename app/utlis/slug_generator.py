import string
from random import choice

ALPHABET: str = string.ascii_letters + string.digits

class SlugGenerator:
    @staticmethod
    def generate() -> str:
        slug = ""
        for _ in range(6):
            slug += choice(ALPHABET)

        return slug

