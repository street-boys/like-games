from fastapi.responses import JSONResponse


def okay_json_response(status_code: int,
                       detail: dict | str,
                       headers: dict[str, str] = None) -> JSONResponse:

    return JSONResponse(status_code=status_code,
                        content={
                            'ok': True,
                            'detail': detail
                        },
                        headers=headers)
