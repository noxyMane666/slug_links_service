import os

from dotenv import load_dotenv

from app.configurations.app_settings import DBSettings

load_dotenv()

class Configuration:
    def __init__(self):
        self.db_settings = self._load_db_settings()

        self._validate_required_fields()

    @staticmethod
    def _load_db_settings() -> DBSettings:
        return DBSettings(
            DB_CONNECTION_STRING=os.getenv("DB_CONNECTION_STRING")
        )

    def _validate_required_fields(self):
        required_fields = {
            "DB_CONNECTION_STRING": self.db_settings.DB_CONNECTION_STRING
        }

        for field_name, value in required_fields.items():
            if not value:
                raise RuntimeError(f"Missing settings param: {field_name}")
