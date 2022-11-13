from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
from sqladmin import Admin
from starlette import status

from api import api_router
from core.config import get_sqladmin_settings
from core.handlers import register_all_exception_handlers
from core.middlewares import register_middlewares
from core.settings import Settings
from core.tools import store
from db.session import _engine
from utils.admin import UserModelView
from utils.backend import Backend


def create_application() -> FastAPI:
    application = FastAPI(
        openapi_url="/api.user/openapi.json",
        docs_url="/api.user/docs",
        redoc_url="/api.user/redoc",
    )
    application.include_router(api_router, prefix="/api.user")

    def setup_admin() -> Admin:
        authentication_backend = Backend(secret_key=get_sqladmin_settings().SQLADMIN_SECRET_KEY)
        admin = Admin(
            app=application,
            engine=_engine,
            base_url="/api.user/admin",
            authentication_backend=authentication_backend,
        )
        admin.add_view(UserModelView)

        return admin

    application.admin = setup_admin()

    @AuthJWT.load_config
    def get_config() -> Settings:
        return Settings()

    @application.on_event(event_type="startup")
    async def startup() -> None:
        await store.connect()

    @application.on_event(event_type="shutdown")
    async def shutdown() -> None:
        await store.disconnect()

    register_all_exception_handlers(app=application)
    register_middlewares(app=application)

    return application


app = create_application()


@app.get(
    path="/api.user",
    status_code=status.HTTP_200_OK,
)
async def root() -> dict:
    return {
        "service": {
            "status": "Okay",
            "health": "Okay",
            "production_ready": True,
        }
    }
