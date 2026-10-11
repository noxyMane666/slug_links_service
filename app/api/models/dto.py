from pydantic import BaseModel, HttpUrl


class GenerationSlugRequestDTO(BaseModel):
    long_url: HttpUrl


class BaseSlugResponseDTO(BaseModel):
    long_url: HttpUrl
    slug: str






