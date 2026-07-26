from pydantic import BaseModel

from app.enums.app_enums import RequestStatus


class SlugGenerationResult(BaseModel):
    slug: str
    status: RequestStatus

class RedirectLookupResult(BaseModel):
    status: RequestStatus





