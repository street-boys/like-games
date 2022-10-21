from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from api import api_router
from core.config import get_database_settings
from core.handlers import register_all_exception_handlers
from core.tools import store


def create_application() -> FastAPI:
    application = FastAPI(openapi_url='/api.profiles/openapi.json',
                          docs_url='/api.profiles/docs',
                          redoc_url='/api.profiles/redoc')
    application.include_router(api_router, prefix='/api.profiles')

    register_all_exception_handlers(application)

    register_tortoise(application,
                      db_url=get_database_settings().PROFILE_DATABASE_URI,
                      modules={
                          'models': ['orm.profile']
                      },
                      generate_schemas=True,
                      add_exception_handlers=True)

    @application.on_event(event_type='startup')
    async def startup() -> None:
        await store.connect()

    @application.on_event(event_type='shutdown')
    async def shutdown() -> None:
        await store.disconnect()

    return application


app = create_application()
