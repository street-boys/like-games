from pydantic import BaseModel


class UserViewSchema(BaseModel):
    id: int
    telegram: int
    username: str
