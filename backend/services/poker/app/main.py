from api import api_router
from fastapi import FastAPI
from responses.okay import okay_response
from starlette import status
from tortoise.contrib.fastapi import register_tortoise

from core.config import get_database_settings
from core.handlers import register_all_exception_handlers
from core.tools import store


def create_application() -> FastAPI:
    application = FastAPI(openapi_url='/api.poker/openapi.json',
                          docs_url='/api.poker/docs',
                          redoc_url='/api.poker/redoc')
    application.include_router(api_router, prefix='/api.poker')

    register_all_exception_handlers(application)

    register_tortoise(application,
                      db_url=get_database_settings().POKER_DATABASE_URI,
                      modules={
                          'models': [
                          ]
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


@app.get(path='/api.poker',
         status_code=status.HTTP_200_OK)
async def root() -> dict:
    return okay_response(detail={
        'service': {
            'status': 'Bad',
            'health': 'Okay',
            'production_ready': False
        }
    })
