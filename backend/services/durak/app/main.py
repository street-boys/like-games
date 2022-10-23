from fastapi import FastAPI
from starlette import status
from tortoise.contrib.fastapi import register_tortoise

from api import api_router
from core.config import get_database_settings
from core.handlers import register_all_exception_handlers
from core.tools import store
from responses.okay import okay_response


def create_application() -> FastAPI:
    application = FastAPI(openapi_url='/api.durak/openapi.json',
                          docs_url='/api.durak/docs',
                          redoc_url='/api.durak/redoc')
    application.include_router(api_router, prefix='/api.durak')

    register_all_exception_handlers(application)

    register_tortoise(application,
                      db_url=get_database_settings().DURAK_DATABASE_URI,
                      modules={
                          'models': [
                              'orm.card',
                              'orm.deck',
                              'orm.game',
                              'orm.user'
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


@app.get(path='/api.profile',
         status_code=status.HTTP_200_OK)
async def root() -> dict:
    return okay_response(detail={
        'service': {
            'status': 'Bad',
            'health': 'Okay',
            'production_ready': False
        }
    })
