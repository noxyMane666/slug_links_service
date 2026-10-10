from dataclasses import dataclass
from enum import Enum


class LogLevels(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

@dataclass(frozen=True)
class DBSettings:
    DB_CONNECTION_STRING: str
    ECHO: bool
    POOL_SIZE: int
    POOL_MAX_OVERFLOW: int
    POOL_TIMEOUT: int

@dataclass(frozen=True)
class LogLevelSetting:
    LOG_LEVEL: LogLevels = LogLevels.INFO