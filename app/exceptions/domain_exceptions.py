class DomainException(Exception):
    pass

class LongUrlNotFoundException(DomainException):
    def __init__(self, slug: str):
        self._slug = slug

    def __str__(self):
        return f"Long url wasn't foud for slug: {self._slug}"

class SlugAlreadyExistsException(DomainException):
    def __init__(self, slug: str):
        self._slug = slug

    def __str__(self):
        return f"The value already exists. Existed slug: {self._slug}"