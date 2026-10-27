from pydantic import Field
from pydantic_settings import BaseSettings

from app.configurations.app_settings import (
    DBSettings,
    LogSetting,
    SlugGeneratingSettings
)


class Configuration(BaseSettings):
    db_settings: DBSettings = Field(default_factory=lambda: DBSettings())
    logger_settings: LogSetting = Field(default_factory=lambda: LogSetting())
    slug_gen_settings: SlugGeneratingSettings = Field(default_factory=lambda: SlugGeneratingSettings())