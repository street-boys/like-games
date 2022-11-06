from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
from starlette import status
from starlette.responses import HTMLResponse

from api import api_router
from core.handlers import register_all_exception_handlers
from core.middlewares import register_middlewares
from core.settings import Settings
from core.tools import store
from responses.okay import okay_response


def create_application() -> FastAPI:
    application = FastAPI(
        openapi_url="/api.user/openapi.json",
        docs_url="/api.user/docs",
        redoc_url="/api.user/redoc",
    )
    application.include_router(api_router, prefix="/api.user")

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


@app.get(path="/api.user", status_code=status.HTTP_200_OK)
async def root() -> dict:
    return okay_response(
        detail={
            "service": {"status": "Okay", "health": "Okay", "production_ready": True}
        }
    )


@app.get(path="/api.user.main")
async def main() -> HTMLResponse:
    return HTMLResponse(
        """<!DOCTYPE html>
<html>
<head>
    <title>Hello, World!</title>
</head>
<body>
    <script async src="https://telegram.org/js/telegram-widget.js?21" data-telegram-login="likegames_poker_tbot" data-size="large" data-auth-url="https://2c43-31-129-207-46.eu.ngrok.io/api.user.telegram.login" data-request-access="write"></script>
</body>
</html>
"""
    )
