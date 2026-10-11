from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.configurations.app_settings import DBSettings, LogLevelSetting


class Configuration(BaseSettings):
    db_settings: DBSettings = Field(default_factory=lambda: DBSettings())
    log_level: LogLevelSetting = Field(default_factory=lambda: LogLevelSetting())

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )