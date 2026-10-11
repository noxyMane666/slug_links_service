from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict


class SlugModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    slug: str
    long_url: str
    redirect_count: int

class SlugUpdateModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    slug: str
    redirect_count: Annotated[int, Field(gt=0)] = 0