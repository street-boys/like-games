from pydantic import BaseModel, EmailStr

from structures.enums import RegistrationTypeEnum


class UserSchema(BaseModel):
    id: int
    telegram: int | None = None
    email: EmailStr
    username: str
    registration_type: RegistrationTypeEnum


class UserViewSchema(BaseModel):
    id: int
    telegram: int | None = None
    username: str
