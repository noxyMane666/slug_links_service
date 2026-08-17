from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import register_routes
from app.configurations.app_config import Configuration
from app.configurations.app_settings import DBSettings
from app.dal.db.database import AppDataBase
from app.handlers.global_exc_handler import register_exception_handler


def build_db_connection(db_settings: DBSettings):
    return AppDataBase(db_settings)

def _make_app_lifespan(config: Configuration):
    @asynccontextmanager
    async def app_lifespan(app: FastAPI):
        app.state.db = build_db_connection(config.db_settings)

        yield

        await app.state.db.close()

    return app_lifespan

def create_app() -> FastAPI:
    config = Configuration()

    app = FastAPI(lifespan=_make_app_lifespan(config))
    register_exception_handler(app)
    register_routes(app)
    return app