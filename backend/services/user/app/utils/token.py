from typing import Any

from fastapi_jwt_auth import AuthJWT


def create_token_and_set_to_cookies(authorize: AuthJWT, subject: Any) -> None:
    access_token, refresh_token = create_token(authorize=authorize, subject=subject)

    set_token_to_cookies(
        authorize=authorize,
        access_token=access_token,
        refresh_token=refresh_token,
    )


def create_token(authorize: AuthJWT, subject: Any) -> tuple[str, str]:
    access_token = authorize.create_access_token(subject=subject)
    refresh_token = authorize.create_refresh_token(subject=subject)

    return access_token, refresh_token


def set_token_to_cookies(
    authorize: AuthJWT,
    access_token: str,
    refresh_token: str,
) -> None:
    authorize.set_access_cookies(access_token)
    authorize.set_refresh_cookies(refresh_token)


def refresh_access_token(authorize: AuthJWT) -> Any:
    current_subject = authorize.get_jwt_subject()

    return authorize.create_access_token(subject=current_subject)


def refresh_and_set_access_token(authorize: AuthJWT) -> Any:
    access_token = refresh_access_token(authorize=authorize)
    authorize.set_access_cookies(access_token)

    return authorize.get_jwt_subject()


def unset_cookies_token(authorize: AuthJWT) -> Any:
    deleted_subject = get_jwt_subject(authorize=authorize)
    authorize.unset_jwt_cookies()

    return deleted_subject


def get_jwt_subject(authorize: AuthJWT) -> Any:
    subject = authorize.get_jwt_subject()

    return subject
