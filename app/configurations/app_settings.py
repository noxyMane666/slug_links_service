from dataclasses import dataclass


@dataclass(frozen=True)
class DBSettings:
    DB_CONNECTION_STRING: str