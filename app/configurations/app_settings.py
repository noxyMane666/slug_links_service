from enum import Enum

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

class LogLevels(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class DBSettings(BaseSettings):
    connection_string: PostgresDsn
    echo: bool = Field(default=False)
    pool_size: int = Field(default=20)
    pool_max_overflow: int = Field(default=10)
    pool_timeout: int = Field(default=30)


class LogSetting(BaseSettings):
    level: LogLevels = Field(default=LogLevels.INFO)


class SlugGeneratingSettings(BaseSettings):
    collision_overflow: int = Field(default=3)