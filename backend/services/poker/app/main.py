from fastapi import FastAPI
from starlette import status

from core.tools import store


def create_application() -> FastAPI:
    application = FastAPI(
        openapi_url="/api.poker/openapi.json",
        docs_url="/api.poker/docs",
        redoc_url="/api.poker/redoc",
    )

    @application.on_event(event_type="startup")
    async def startup() -> None:
        await store.connect()

    @application.on_event(event_type="shutdown")
    async def shutdown() -> None:
        await store.disconnect()

    return application


app = create_application()


@app.get(path="/api.poker", status_code=status.HTTP_200_OK)
async def root() -> dict:
    return {"service": {"status": "Bad", "health": "Okay", "production_ready": False}}
