from pydantic import BaseModel, HttpUrl


class GenerationSlugRequestDTO(BaseModel):
    long_url: HttpUrl

class GetLongLinkDTO(BaseModel):
    slug: str

class SlugGenerationResultDTO(BaseModel):
    slug: str

class RedirectLookupResultDTO(BaseModel):
    long_url: HttpUrl






