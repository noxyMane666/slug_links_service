from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import register_routes
from app.configurations.app_config import Configuration
from app.dal.db.database import AppDataBase


def build_db_connection(config: Configuration):
    return AppDataBase(config.db_connection_string)

def _make_app_lifespan(config: Configuration):
    @asynccontextmanager
    async def app_lifespan(app: FastAPI):
        app.state.db = build_db_connection(config)

        yield

        await app.state.db.close()

    return app_lifespan

def create_app() -> FastAPI:
    config = Configuration()

    app = FastAPI(lifespan=_make_app_lifespan(config))
    register_routes(app)
    return app