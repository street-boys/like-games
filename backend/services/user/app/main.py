from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
from starlette import status
from tortoise.contrib.fastapi import register_tortoise

from api import api_router
from core.config import get_database_settings
from core.handlers import register_all_exception_handlers
from core.settings import Settings
from responses.okay import okay_response


def create_application() -> FastAPI:
    application = FastAPI(openapi_url='/api.user/openapi.json',
                          docs_url='/api.user/docs',
                          redoc_url='/api.user/redoc')
    application.include_router(api_router, prefix='/api.users')

    @AuthJWT.load_config
    def get_config() -> Settings:
        return Settings()

    register_all_exception_handlers(application)

    register_tortoise(application,
                      db_url=get_database_settings().USER_DATABASE_URI,
                      modules={
                          'models': ['orm.user']
                      },
                      generate_schemas=True,
                      add_exception_handlers=True)

    return application


app = create_application()


@app.get(path='/api.user',
         status_code=status.HTTP_200_OK)
async def root() -> dict:
    return okay_response(detail={
        'service': {
            'status': 'Okay',
            'health': 'Okay',
            'production_ready': True
        }
    })
