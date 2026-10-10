from contextlib import asynccontextmanager
from logging import getLogger

from fastapi import FastAPI

from app.api.routes import register_routes
from app.configurations.app_config import Configuration
from app.configurations.app_settings import DBSettings
from app.core.dal.db.database import AppDataBase
from app.core.handlers.global_exc_handler import register_exception_handler
from app.logging.logger_setup import setup_logging
from app.middleware.request_logging_middleware import register_logging_middleware

logger = getLogger(__name__)


def create_app_lifespan(config: Configuration):
    @asynccontextmanager
    async def app_lifespan(app: FastAPI):
        db = AppDataBase(config.db_settings)

        try:
            await db.check_db_connection()
            app.state.db = db
        except Exception as e:
            logger.error("Database connection failed on startup", exc_info=e)
            await db.close()
            raise RuntimeError("Couldn't connect to database") from e

        logger.info("Database connection established")
        yield

        await app.state.db.close()
        logger.info("Database connection closed")

    return app_lifespan

def create_app() -> FastAPI:
    config = Configuration()
    setup_logging(config.log_level_settings.LOG_LEVEL.value)

    app = FastAPI(lifespan=create_app_lifespan(config))
    register_exception_handler(app)
    register_logging_middleware(app)
    register_routes(app)
    return app