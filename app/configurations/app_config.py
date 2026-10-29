from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.configurations.app_settings import (
    DBSettings,
    LogSetting,
    SlugGeneratingSettings
)


class Configuration(BaseSettings):
    db_settings: DBSettings = Field(default_factory=DBSettings)
    log_settings: LogSetting = Field(default_factory=LogSetting)
    slug_gen_settings: SlugGeneratingSettings = Field(default_factory=SlugGeneratingSettings)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore"
    )