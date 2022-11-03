from fastapi.requests import Request

from db.session import session


def get_session(request: Request) -> session:
    return request.state.session
