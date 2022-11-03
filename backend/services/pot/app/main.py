from fastapi import FastAPI
from starlette import status

from api import api_router
from core.handlers import register_all_exception_handlers
from core.middlewares import register_middlewares
from core.tools import store
from responses.okay import okay_response


def create_application() -> FastAPI:
    application = FastAPI(
        openapi_url="/api.pot/openapi.json",
        docs_url="/api.pot/docs",
        redoc_url="/api.pot/redoc",
    )
    application.include_router(api_router, prefix="/api.pot")

    register_all_exception_handlers(app=application)
    register_middlewares(app=application)

    @application.on_event(event_type="startup")
    async def startup() -> None:
        await store.connect()

    @application.on_event(event_type="shutdown")
    async def shutdown() -> None:
        await store.disconnect()

    return application


app = create_application()


@app.get(path="/api.profile", status_code=status.HTTP_200_OK)
async def root() -> dict:
    return okay_response(
        detail={
            "service": {"status": "Okay", "health": "Okay", "production_ready": True}
        }
    )
