from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
from tortoise.contrib.fastapi import register_tortoise

from api import api_router
from core.config import get_database_settings
from core.handlers import register_all_exception_handlers
from core.settings import Settings


def create_application() -> FastAPI:
    application = FastAPI(openapi_url='/api.users/openapi.json',
                          docs_url='/api.users/docs',
                          redoc_url='/api.users/redoc')
    application.include_router(api_router, prefix='/api.users')

    @AuthJWT.load_config
    def get_config() -> Settings:
        return Settings()

    register_all_exception_handlers(application)

    register_tortoise(application,
                      db_url=get_database_settings().USERS_DATABASE_URI,
                      modules={
                          'models': ['orm.user']
                      },
                      generate_schemas=True,
                      add_exception_handlers=True)

    return application


app = create_application()
