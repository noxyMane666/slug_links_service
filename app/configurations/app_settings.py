from dataclasses import dataclass


@dataclass(frozen=True)
class DBSettings:
    DB_CONNECTION_STRING: str
    ECHO: bool
    POOL_SIZE: int
    POOL_MAX_OVERFLOW: int
    POOL_TIMEOUT: int    