from logging import getLogger

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException

from responses.bad import bad_response

logger = getLogger(__name__)


def register_authjwtexception_handler(app: FastAPI) -> None:
    @app.exception_handler(AuthJWTException)
    async def authjwt_exception_handler(
        request: Request, exc: AuthJWTException
    ) -> JSONResponse:
        logger.info(
            f"With request=([{request.method}][{request.url}][{request.query_params}]) "
            f"occurred error=([{exc.status_code}][{exc.message}])"
        )

        return bad_response(status_code=exc.status_code, detail=exc.message)


def register_httpexception_handler(app: FastAPI) -> None:
    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request, exc: HTTPException
    ) -> JSONResponse:
        logger.info(
            f"With request=([{request.method}][{request.url}][{request.query_params}]) "
            f"occurred error=([{exc.status_code}][{exc.detail}])"
        )

        return bad_response(status_code=exc.status_code, detail={"detail": exc.detail})


def register_all_exception_handlers(app: FastAPI) -> None:
    register_authjwtexception_handler(app)
    register_httpexception_handler(app)
