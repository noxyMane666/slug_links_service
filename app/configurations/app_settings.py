from enum import Enum

from pydantic import BaseModel, Field, PostgresDsn


class LogLevels(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class DBSettings(BaseModel):
    connection_string: PostgresDsn = Field(alias="DB_CONNECTION_STRING")
    echo: bool = Field(default=False, alias="DB_ECHO")
    pool_size: int = Field(default=20, alias="DB_MAX_POOL_SIZE")
    pool_max_overflow: int = Field(default=10, alias="DB_POOL_MAX_OVERFLOW")
    pool_timeout: int = Field(default=30, alias="DB_POOL_TIMEOUT")


class LogSetting(BaseModel):
    log_level: LogLevels = Field(default=LogLevels.INFO, alias="LOG_LEVEL")


class SlugGeneratingSettings(BaseModel):
    generation_collision_overflow: int = Field(default=3, alias="SLUGGEN_COLLISION_OVERFLOW")