from pydantic import BaseModel

from core.config import get_jwt_settings


class Settings(BaseModel):
    authjwt_secret_key: str = get_jwt_settings().SECRET_KEY
    authjwt_algorithm: str = get_jwt_settings().ALGORITHM

    authjwt_token_location: set = {"cookies", "headers"}

    authjwt_cookie_secure: bool = False

    authjwt_cookie_csrf_protect: bool = True
