from pydantic import BaseModel, Field, ConfigDict


class SlugModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    slug: str
    long_url: str
    redirect_count: int | None

class SlugUpdateModel(BaseModel):
    slug: str
    redirect_count: int = Field(gt=0)