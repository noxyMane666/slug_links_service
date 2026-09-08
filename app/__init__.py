from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError

from app.api.routes import register_routes
from app.configurations.app_config import Configuration
from app.configurations.app_settings import DBSettings
from app.core.dal.db.database import AppDataBase
from app.core.handlers.global_exc_handler import register_exception_handler


def build_db_connection(db_settings: DBSettings) -> AppDataBase:
    return AppDataBase(db_settings)

def create_app_lifespan(config: Configuration):
    @asynccontextmanager
    async def app_lifespan(app: FastAPI):
        db = build_db_connection(config.db_settings)

        try:
            await db.check_db_connection()
            app.state.db = db
        except SQLAlchemyError as e:
            await db.close()
            raise RuntimeError("Couldn't connect to database") from e

        yield

        await app.state.db.close()

    return app_lifespan

def create_app() -> FastAPI:
    config = Configuration()

    app = FastAPI(lifespan=create_app_lifespan(config))
    register_exception_handler(app)
    register_routes(app)
    return app