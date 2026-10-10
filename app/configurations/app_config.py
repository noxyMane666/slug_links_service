import os

from dotenv import load_dotenv

from app.configurations.app_settings import DBSettings, LogLevelSetting, LogLevels

load_dotenv()

class Configuration:
    def __init__(self):
        self.db_settings = self._load_db_settings()
        self.log_level_settings = self._load_ll_settings()

        self._validate_required_fields()

    @staticmethod
    def _load_db_settings() -> DBSettings:
        return DBSettings(
            DB_CONNECTION_STRING=os.getenv("DB_CONNECTION_STRING"),
            ECHO=os.getenv("DB_ECHO", "false").lower == "true",
            POOL_SIZE=int(os.getenv("DB_MAX_POOL_SIZE", "20")),
            POOL_MAX_OVERFLOW=int(os.getenv("DB_POOL_MAX_OVERFLOW", "10")),
            POOL_TIMEOUT=int(os.getenv("DB_POOL_TIMEOUT", "30"))
        )

    @staticmethod
    def _load_ll_settings() -> LogLevelSetting:
        log_level = os.getenv("LOG_LEVEL", "INFO")
        return LogLevelSetting(
            LOG_LEVEL=LogLevels(log_level)
        )

    def _validate_required_fields(self):
        required_fields = {
            "DB_CONNECTION_STRING": self.db_settings.DB_CONNECTION_STRING
        }

        for field_name, value in required_fields.items():
            if not value:
                raise RuntimeError(f"Missing settings param: {field_name}")
