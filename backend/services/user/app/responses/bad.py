from fastapi.responses import JSONResponse


def bad_response(status_code: int, detail: dict) -> JSONResponse:
    return JSONResponse(
        status_code=status_code, content={"ok": False, "detail": detail}
    )
